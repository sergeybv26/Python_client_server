"""
Программа-клиент
"""
import json
import time
from socket import socket, AF_INET, SOCK_STREAM

from common.utils import get_tcp_parameters, send_message, get_message
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR


def create_presence(account_name='Guest'):
    """
    Формирует запрос на сервер о присутствии клиента
    :param account_name: Имя пользователя
    :return: JIM объект
    """

    request = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }

    return request


def process_answ(message):
    """
    Разбирает ответ от сервера
    :param message: Сообщение ответа
    :return: код ответа и сообщение (при наличии)
    """

    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400: {message[ERROR]}'
    raise ValueError


def main():
    """
    Главная функция клиента.
    Параметры принимаются из командной строки (-p - номер порта, -а - адрес),
    если параметров нет - принимаются параметры по умолчанию
    :return:
    """
    param = get_tcp_parameters()

    server_address = param.a
    server_port = int(param.p)
    print(server_port)

    client = socket(AF_INET, SOCK_STREAM)
    client.connect((server_address, server_port))

    message_to_server = create_presence()

    send_message(client, message_to_server)

    try:
        answer = process_answ(get_message(client))
        print(answer)
    except (ValueError, json.JSONDecodeError):
        print('Не удалось распознать сообщение от сервера')

    client.close()


if __name__ == '__main__':
    main()
