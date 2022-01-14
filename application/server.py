"""
Программа-сервер
"""
import json
from socket import socket, AF_INET, SOCK_STREAM

from common.utils import get_tcp_parameters, get_message, send_message
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, MAX_CONNECTIONS


def process_client_message(message):
    """
    Обрабатывает сообщения от клиентов
    :param message: сообщение от клиента
    :return: словарь-ответ
    """

    if ACTION in message and message[ACTION] == PRESENCE and TIME in message and \
            USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad request'
    }


def main():
    """
    Главная функция сервера.
    Параметры принимаются из командной строки (-p - номер порта, -а - адрес),
    если параметров нет - принимаются параметры по умолчанию
    :return:
    """

    param = get_tcp_parameters(True)

    listen_address = param.a
    listen_port = int(param.p)
    print(listen_port)

    transport = socket(AF_INET, SOCK_STREAM)
    transport.bind((listen_address, listen_port))
    transport.listen(MAX_CONNECTIONS)

    while True:
        client, client_address = transport.accept()

        try:
            message_from_client = get_message(client)
            print(message_from_client)
            response = process_client_message(message_from_client)
            send_message(client, response)
            client.close()
        except (ValueError, json.JSONDecodeError):
            print('Принято не корректное сообщение от клиента')
            client.close()


if __name__ == '__main__':
    main()
