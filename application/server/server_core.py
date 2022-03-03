"""
Основной компонент сервера.
Принимает соединения, принимает и обрабатывает сообщения
"""
import binascii
import hmac
import json
import logging
import os
import socket
import sys
import threading
from select import select

sys.path.append('../')
from common.decos import login_required
from common.descrptrs import Port
from common.metaclasses import ServerMaker
from common.utils import get_message, send_message
from common.variables import MAX_CONNECTIONS, RECEIVER, SENDER, ACTION, PRESENCE, TIME, USER, MESSAGE, MESSAGE_TEXT, \
    RESPONSE, RESPONSE_400, ERROR, ACCOUNT_NAME, QUIT, GET_CONTACTS, RESPONSE_202, LIST_INFO, ADD_CONTACT, \
    REMOVE_CONTACT, USERS_REQUEST, PUBLIC_KEY_REQUEST, RESPONSE_511, DATA, PUBLIC_KEY, RESPONSE_205


class Server(threading.Thread, metaclass=ServerMaker):
    port = Port()

    def __init__(self, listen_address, listen_port, database):
        self.addr = listen_address
        self.port = listen_port
        self.logger = logging.getLogger('server')
        self.clients = []
        self.messages = []
        self.names = {}
        self.sock = None
        self.database = database
        self.listen_sockets = None
        self.error_sockets = None
        self.running = True
        super().__init__()

    def init_socket(self):
        """
        Инициализирует сокет
        :return: None
        """
        self.logger.info(f'Запущен сервер. Порт для подключений: {self.port}.'
                         f'Подключения принимаются с адреса: {self.addr}. '
                         f'Если адрес не указан, соединения принимаются с любых адресов')
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        transport.bind((self.addr, self.port))
        transport.settimeout(0.5)

        self.sock = transport
        self.sock.listen(MAX_CONNECTIONS)

    def run(self):
        """
        Основной цикл сервера
        :return: None
        """
        self.init_socket()

        while self.running:
            try:
                client, client_address = self.sock.accept()
            except OSError:
                pass
            else:
                self.logger.info(f'Установлено соединение с клиентом {client_address}')
                client.settimeout(5)
                self.clients.append(client)

            recv_data_list = []
            send_data_list = []
            err_list = []

            try:
                if self.clients:
                    recv_data_list, send_data_list, err_list = select(self.clients, self.clients, [], 0)
            except OSError as err:
                self.logger.error(f'Ошибка работы с сокетами: {err}')

            if recv_data_list:
                for client_with_msg in recv_data_list:
                    try:
                        self.process_client_message(get_message(client_with_msg), client_with_msg)
                    except (OSError, TypeError, json.JSONDecodeError) as err:
                        self.logger.info(f'Ошибка получения сообщения от клиента: {err}')
                        self.remove_client(client_with_msg)

    def remove_client(self, client):
        """
        Осуществляет обработку клиента, с которым прервалась связь или который передает сообщение о выходе
        :param client: сокет клиента
        :return: None
        """
        self.logger.info(f'Клиент {client.getpeername()} отключился от сервера')
        for name in self.names:
            if self.names[name] == client:
                self.database.user_logout(name)
                del self.names[name]
                break
        self.clients.remove(client)
        client.close()

    def process_message(self, message):
        """
        Выполняет отправку сообщения определенному клиенту
        :param message: Сообщение в виде словаря
        :return: None
        """
        if message[RECEIVER] in self.names.keys() and self.names[message[RECEIVER]] in self.listen_sockets:
            try:
                send_message(self.names[message[RECEIVER]], message)
                self.logger.info(f'Отправлено сообщение пользователю {message[RECEIVER]} от '
                                 f'пользователя {message[SENDER]}.')
            except OSError:
                self.remove_client(self.names[message[RECEIVER]])
        elif message[RECEIVER] in self.names.keys() and self.names[message[RECEIVER]] not in self.listen_sockets:
            self.logger.error(f'Связь с клиентом {message[RECEIVER]} была потеряна. '
                              f'Соединение закрыто, доставка невозможна.')
            self.remove_client(self.names[message[RECEIVER]])
        else:
            self.logger.error(f'Пользователь {message[RECEIVER]} не зарегистрирован на сервере. '
                              f'Отправка сообщения не возможна')

    @login_required
    def process_client_message(self, message, client):
        """
        Обрабатывает сообщения от клиентов.
        Если это сообщение о присутствии - проверяет корректность и отправляет ответ клиенту.
        Если это сообщение пользователям - проверяет корректность и добавляет в очередь
        :param message: сообщение от клиента
        :param client: сокет с клиентом
        :return: None
        """
        self.logger.debug(f'Разбор сообщения {message} от клиента')

        if ACTION in message and message[ACTION] == PRESENCE and TIME in message and \
                USER in message:
            self.user_authorization(message, client)
        elif ACTION in message and message[ACTION] == MESSAGE and \
                RECEIVER in message and SENDER in message and \
                TIME in message and MESSAGE_TEXT in message and \
                self.names[message[SENDER]] == client:
            if message[RECEIVER] in self.names:
                self.process_message(message)
                self.database.process_message(message[SENDER], message[RECEIVER])
                try:
                    send_message(client, {RESPONSE: 200})
                except OSError:
                    self.remove_client(client)
            else:
                response = RESPONSE_400
                response[ERROR] = 'Получатель не зарегистрирован на сервере'
                try:
                    send_message(client, response)
                except OSError:
                    self.remove_client(client)
            return
        elif ACTION in message and ACCOUNT_NAME in message and message[ACTION] == QUIT and \
                self.names[message[ACCOUNT_NAME]] == client:
            self.logger.debug(f'Соединение с клиентом {message[ACCOUNT_NAME]} закрывается по инициативе клиента')
            self.remove_client(client)
        elif ACTION in message and message[ACTION] == GET_CONTACTS and USER in message and \
                self.names[message[USER]] == client:
            response = RESPONSE_202
            response[LIST_INFO] = self.database.get_contacts(message[USER])
            try:
                send_message(client, response)
            except OSError:
                self.remove_client(client)
        elif ACTION in message and message[ACTION] == ADD_CONTACT and ACCOUNT_NAME in message and \
                USER in message and self.names[message[USER]] == client:
            self.database.add_contact(message[USER], message[ACCOUNT_NAME])
            try:
                send_message(client, {RESPONSE: 200})
            except OSError:
                self.remove_client(client)
        elif ACTION in message and message[ACTION] == REMOVE_CONTACT and ACCOUNT_NAME in message and \
                USER in message and self.names[message[USER]] == client:
            self.database.remove_contact(message[USER], message[ACCOUNT_NAME])
            try:
                send_message(client, {RESPONSE: 200})
            except OSError:
                self.remove_client(client)
        elif ACTION in message and message[ACTION] == USERS_REQUEST and ACCOUNT_NAME in message and \
                self.names[message[ACCOUNT_NAME]] == client:
            response = RESPONSE_202
            response[LIST_INFO] = [user[0] for user in self.database.users_list()]
            try:
                send_message(client, response)
            except OSError:
                self.remove_client(client)
        elif ACTION in message and message[ACTION] == PUBLIC_KEY_REQUEST and ACCOUNT_NAME in message:
            response = RESPONSE_511
            response[DATA] = self.database.get_public_key(message[ACCOUNT_NAME])
            if response[DATA]:
                try:
                    send_message(client, response)
                except OSError:
                    self.remove_client(client)
            else:
                response = RESPONSE_400
                response[ERROR] = 'Нет публичного ключа для данного пользователя'
                try:
                    send_message(client, response)
                except OSError:
                    self.remove_client(client)
        else:
            response = RESPONSE_400
            response[ERROR] = 'Получен некорректный запрос'
            try:
                send_message(client, response)
            except OSError:
                self.remove_client(client)

    def user_authorization(self, message, sock):
        """
        Осуществляет авторизацию пользователей
        :param message: сообщение об авторизации от пользователя
        :param sock: сокет
        :return: None
        """
        self.logger.debug(f'Выполняется авторизация пользователя {message[USER]}')
        if message[USER][ACCOUNT_NAME] in self.names.keys():
            response = RESPONSE_400
            response[ERROR] = 'Имя пользователя уже занято'
            try:
                send_message(sock, response)
                self.logger.debug(f'Имя пользователя уже занято. Отправка сообщения')
            except OSError:
                pass
            self.clients.remove(sock)
            sock.close()
        elif not self.database.check_user(message[USER][ACCOUNT_NAME]):
            response = RESPONSE_400
            response[ERROR] = 'Пользователь не зарегистрирован'
            try:
                send_message(sock, response)
                self.logger.debug(f'Отправка сообщения: Пользователь не зарегистрирован')
            except OSError:
                pass
            self.clients.remove(sock)
            sock.close()
        else:
            self.logger.debug(f'Начата проверка пароля пользователя {message[USER][ACCOUNT_NAME]}')
            auth_message = RESPONSE_511
            random_str = binascii.hexlify(os.urandom(64))
            auth_message[DATA] = random_str.decode('ascii')
            verify_hash = hmac.new(self.database.get_password(message[USER][ACCOUNT_NAME]), random_str, 'MD5')
            verify_digest = verify_hash.digest()
            self.logger.debug(f'Сформировано сообщение атентификации: {auth_message}')
            try:
                send_message(sock, auth_message)
                answer = get_message(sock)
            except OSError as err:
                self.logger.debug(f'Ошибка обмена сообщениями аутентификации: {err}')
                sock.close()
                return
            client_digest = binascii.a2b_base64(answer[DATA])
            if RESPONSE in answer and answer[RESPONSE] == 511 and \
                    hmac.compare_digest(verify_digest, client_digest):
                self.names[message[USER][ACCOUNT_NAME]] = sock
                client_ip, client_port = sock.getpeername()
                try:
                    send_message(sock, {RESPONSE: 200})
                except OSError:
                    self.remove_client(message[USER][ACCOUNT_NAME])
                self.database.user_login(
                    message[USER][ACCOUNT_NAME],
                    client_ip,
                    client_port,
                    message[USER][PUBLIC_KEY]
                )
            else:
                response = RESPONSE_400
                response[ERROR] = 'Неверный пароль'
                try:
                    send_message(sock, response)
                except OSError:
                    pass
                self.clients.remove(sock)
                sock.close()

    def service_update_lists(self):
        """
        Отправляет сообщение 205 клиентам о необходимости обновить справочники
        :return: None
        """
        for client in self.names:
            try:
                send_message(self.names[client], RESPONSE_205)
            except OSError:
                self.remove_client(self.names[client])


if __name__ == '__main__':
    pass
