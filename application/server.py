"""
Программа-сервер. Объектно-ориентированный стиль
"""
import argparse
import configparser
import logging
import os.path
import sys
import threading
import time
from select import select
import socket

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMessageBox

from common.utils import get_message, send_message, get_parameters
from common.variables import MAX_CONNECTIONS, RECEIVER, SENDER, ACTION, MESSAGE, TIME, MESSAGE_TEXT, PRESENCE, USER, \
    ACCOUNT_NAME, RESPONSE, RESPONSE_400, ERROR, QUIT, GET_CONTACTS, RESPONSE_202, LIST_INFO, ADD_CONTACT, \
    REMOVE_CONTACT, USERS_REQUEST, SERVER_CONFIG
from descrptrs import Port
from errors import IncorrectDataReceivedError, MissingClient
from metaclasses import ServerMaker
import log.server_log_config
from server_db import ServerDB
from server_gui import MainWindow, gui_create_model, StatisticWindow, create_stat_model, ConfigWindow

stat_window = None
config_window = None
new_connection = False
conflag_lock = threading.Lock()


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
        super().__init__()

    def init_socket(self):
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
        global new_connection
        self.init_socket()

        while True:
            try:
                client, client_address = self.sock.accept()
            except OSError:
                pass
            else:
                self.logger.info(f'Установлено соединение с клиентом {client_address}')
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
                    except OSError:
                        self.logger.info(f'Клиент {client_with_msg.getpeername()} отключился от сервера')
                        for name in self.names:
                            if self.names[name] == client_with_msg:
                                self.database.user_logout(name)
                                del self.names[name]
                                break
                        self.clients.remove(client_with_msg)
                        with conflag_lock:
                            new_connection = True

            for msg in self.messages:
                try:
                    self.process_message(msg, send_data_list)
                except (ConnectionError, ConnectionAbortedError, ConnectionResetError,
                        ConnectionRefusedError, TypeError):
                    self.logger.error(f'Связь с клиентом {msg[RECEIVER]} была потеряна.')
                    self.clients.remove(self.names[msg[RECEIVER]])
                    self.database.user_logout(msg[RECEIVER])
                    del self.names[msg[RECEIVER]]
                    with conflag_lock:
                        new_connection = True
            self.messages.clear()

    def process_message(self, message, listen_socks):
        """
        Выполняет отправку сообщения определенному клиенту
        :param message: Сообщение в виде словаря
        :param listen_socks: список сокетов
        :return: None
        """
        if message[RECEIVER] in self.names.keys() and self.names[message[RECEIVER]] in listen_socks:
            send_message(self.names[message[RECEIVER]], message)
            self.logger.info(f'Отправлено сообщение пользователю {message[RECEIVER]} от '
                             f'пользователя {message[SENDER]}.')
        elif message[RECEIVER] in self.names.keys() and self.names[message[RECEIVER]] not in listen_socks:
            raise ConnectionError
        else:
            response_error = {
                ACTION: MESSAGE,
                SENDER: 'Сервер мессенджера',
                RECEIVER: message[SENDER],
                TIME: time.time(),
                MESSAGE_TEXT: f'Пользователь {message[RECEIVER]} не зарегистрирован на сервере. '
                              f'Отправка сообщения не возможна'
            }
            send_message(self.names[message[SENDER]], response_error)
            self.logger.error(f'Пользователь {message[RECEIVER]} не зарегистрирован на сервере. '
                              f'Отправка сообщения не возможна')

    def process_client_message(self, message, client):
        """
        Обрабатывает сообщения от клиентов.
        Если это сообщение о присутствии - проверяет корректность и отправляет ответ клиенту.
        Если это сообщение пользователям - проверяет корректность и добавляет в очередь
        :param message: сообщение от клиента
        :param client: сокет с клиентом
        :return: None
        """
        global new_connection
        self.logger.debug(f'Разбор сообщения {message} от клиента')

        if ACTION in message and message[ACTION] == PRESENCE and TIME in message and \
                USER in message:
            if message[USER][ACCOUNT_NAME] not in self.names.keys():
                self.names[message[USER][ACCOUNT_NAME]] = client
                client_ip, client_port = client.getpeername()
                self.database.user_login(message[USER][ACCOUNT_NAME], client_ip, client_port)
                send_message(client, {RESPONSE: 200})
                with conflag_lock:
                    new_connection = True
            else:
                response = RESPONSE_400
                response[ERROR] = 'Имя пользователя уже занято'
                send_message(client, response)
                self.clients.remove(client)
                client.close()
            return
        elif ACTION in message and message[ACTION] == MESSAGE and \
                RECEIVER in message and SENDER in message and \
                TIME in message and MESSAGE_TEXT in message:
            self.messages.append(message)
            self.database.process_message(message[SENDER], message[RECEIVER])
            send_message(client, {RESPONSE: 200})
            return
        elif ACTION in message and ACCOUNT_NAME in message and message[ACTION] == QUIT and \
                message[ACCOUNT_NAME] in self.names.keys():
            self.database.user_logout(message[ACCOUNT_NAME])
            self.clients.remove(self.names[message[ACCOUNT_NAME]])
            self.logger.debug(f'Соединение с клиентом {message[ACCOUNT_NAME]} закрывается по инициативе клиента')
            self.names[message[ACCOUNT_NAME]].close()
            del self.names[message[ACCOUNT_NAME]]
            with conflag_lock:
                new_connection = True
            return
        elif ACTION in message and message[ACTION] == GET_CONTACTS and USER in message and \
                self.names[message[USER]] == client:
            response = RESPONSE_202
            response[LIST_INFO] = self.database.get_contacts(message[USER])
            send_message(client, response)
        elif ACTION in message and message[ACTION] == ADD_CONTACT and ACCOUNT_NAME in message and \
                USER in message and self.names[message[USER]] == client:
            self.database.add_contact(message[USER], message[ACCOUNT_NAME])
            send_message(client, {RESPONSE: 200})
        elif ACTION in message and message[ACTION] == REMOVE_CONTACT and ACCOUNT_NAME in message and \
                USER in message and self.names[message[USER]] == client:
            self.database.remove_contact(message[USER], message[ACCOUNT_NAME])
            send_message(client, {RESPONSE: 200})
        elif ACTION in message and message[ACTION] == USERS_REQUEST and ACCOUNT_NAME in message and \
                self.names[message[ACCOUNT_NAME]] == client:
            response = RESPONSE_202
            response[LIST_INFO] = [user[0] for user in self.database.users_list()]
            send_message(client, response)
        else:
            response = RESPONSE_400
            response[ERROR] = 'Получен некорректный запрос'
            send_message(client, response)
            raise IncorrectDataReceivedError


def get_server_parameters(default_address, default_port):
    """
    Получает параметры работы сервера из командной строки
    :param default_address: IP адрес по умолчанию, который слушает сервер
    :param default_port: порт по умолчанию
    :return: кортеж - параметры работы сервера
    """
    parser_param = argparse.ArgumentParser()

    parser_param.add_argument('-a', default=default_address, nargs='?')
    parser_param.add_argument('-p', default=default_port, type=int, nargs='?')

    parameters = parser_param.parse_args(sys.argv[1:])
    listen_address = parameters.a
    listen_port = parameters.p

    return listen_address, listen_port


def print_help():
    """
    Печатает справку по командам для сервера
    :return: None
    """
    print('Поддерживаемые команды:')
    print('users - спсиок известных пользователей')
    print('connected - список подключенных пользователей')
    print('loghist - история входов пользователя')
    print('exit - завершение работы сервера')
    print('help - вывод справки по поддерживаемым командам')


def main():
    """
    Функция, которая получает параметры командной строки и запускает сервер
    :return: None
    """
    config = configparser.ConfigParser()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config.read(f"{dir_path}/{SERVER_CONFIG}")

    listen_address, listen_port = get_server_parameters(config['SETTINGS']['listen_address'],
                                                        config['SETTINGS']['default_port'])
    database = ServerDB(
        os.path.join(
            config['SETTINGS']['database_path'],
            config['SETTINGS']['database_file']
        )
    )

    server = Server(listen_address, listen_port, database)
    server.daemon = True
    server.start()

    server_app = QApplication(sys.argv)
    main_window = MainWindow()

    main_window.statusBar().showMessage('Server is running...')
    main_window.active_clients_table.setModel(gui_create_model(database))
    main_window.active_clients_table.resizeColumnsToContents()
    main_window.active_clients_table.resizeRowsToContents()

    def active_clients_update():
        """
        Проверяет флаг подключения м обновляет список подключенных
        :return: None
        """
        global new_connection
        if new_connection:
            main_window.active_clients_table.setModel(gui_create_model(database))
            main_window.active_clients_table.resizeColumnsToContents()
            main_window.active_clients_table.resizeRowsToContents()
            with conflag_lock:
                new_connection = False

    def show_statistic():
        """
        Создает окно статики
        :return: None
        """
        global stat_window
        stat_window = StatisticWindow()
        stat_window.statistic_table.setModel(create_stat_model(database))
        stat_window.statistic_table.resizeColumnsToContents()
        stat_window.statistic_table.resizeRowsToContents()
        stat_window.show()

    def server_config():
        """
        Создает окно с настройками сервера
        :return: None
        """
        global config_window
        config_window = ConfigWindow()
        config_window.db_path.insert(config['SETTINGS']['database_path'])
        config_window.db_file.insert(config['SETTINGS']['database_file'])
        config_window.port.insert(config['SETTINGS']['default_port'])
        config_window.ip.insert(config['SETTINGS']['listen_address'])
        config_window.save_button.clicked.connect(save_server_config)

    def save_server_config():
        """
        Сохраняет настройки сервера
        :return: None
        """
        global config_window
        message = QMessageBox()
        config['SETTINGS']['database_path'] = config_window.db_path.text()
        config['SETTINGS']['database_file'] = config_window.db_file.text()
        try:
            port = int(config_window.port.text())
        except ValueError:
            message.warning(config_window, 'Ошибка', 'Порт должен быть числом')
        else:
            config['SETTINGS']['listen_address'] = config_window.ip.text()
            if 1023 < port < 65536:
                config['SETTINGS']['default_port'] = str(port)
                with open(f"{dir_path}/{SERVER_CONFIG}", 'w') as conf:
                    config.write(conf)
                    message.information(config_window, 'ОК', 'Настройки успешно сохранены')
            else:
                message.warning(config_window, 'Ошибка', 'Порт должен быть от 1024 до 65535')

    timer = QTimer()
    timer.timeout.connect(active_clients_update)
    timer.start(1000)

    main_window.refresh_button.triggered.connect(active_clients_update)
    main_window.show_statistic_button.triggered.connect(show_statistic)
    main_window.config_button.triggered.connect(server_config)

    server_app.exec_()


if __name__ == '__main__':
    main()
