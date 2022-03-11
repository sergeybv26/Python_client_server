"""
Программа-клиент.
"""
import argparse
import logging
import os.path
import sys

from Cryptodome.PublicKey import RSA
from PyQt5.QtWidgets import QApplication, QMessageBox

from client.client_db import ClientDB
from client.dialog_start import UserNameDialog
from client.main_window import ClientMainWindow
from client.transport import ClientTransport
from common.errors import ServerError
from common.decos import log
from common.variables import DEFAULT_IP_ADDRESS, DEFAULT_PORT

CLIENT_LOGGER = logging.getLogger('client')


@log
def check_client_parameters():
    """
    Выполняет проверку параметров клиента

    :return: Кортеж - параметры клиента
    """
    parser_param = argparse.ArgumentParser()

    parser_param.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser_param.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser_param.add_argument('-n', '--name', default=None, nargs='?')
    parser_param.add_argument('-p', '--password', default='', nargs='?')

    params = parser_param.parse_args(sys.argv[1:])
    _server_address, _server_port, _client_name, _client_password = params.addr, params.port, \
                                                                    params.name, params.password

    if not 1023 < _server_port < 65536:
        CLIENT_LOGGER.critical(f'Попытка запуска клиента с неподходящим номером порта '
                               f'{_server_port}. Допустимые номера порта: от 1024 до 65535. '
                               f'Клиент завершается.')
        sys.exit(1)

    return _server_address, _server_port, _client_name, _client_password


if __name__ == '__main__':
    """Осуществляет запуск приложения-клиента"""
    CLIENT_LOGGER.info('Запущено приложение')

    server_address, server_port, client_name, client_password = check_client_parameters()

    client_app = QApplication(sys.argv)

    start_dialog = UserNameDialog()

    if not client_name or not client_password:
        client_app.exec_()
        if start_dialog.ok_pressed:
            client_name = start_dialog.client_name.text()
            client_password = start_dialog.client_password.text()
            CLIENT_LOGGER.debug(f'Введены параметры: username: {client_name}, password: {client_password}')
        else:
            exit(0)

    CLIENT_LOGGER.info(f'Запущен клиент с парамтрами: '
                       f'адрес сервера - {server_address}, '
                       f'порт - {server_port}, '
                       f'имя пользователя - {client_name}.')

    dir_path = os.path.dirname(os.path.realpath(__file__))
    key_file = os.path.join(dir_path, f'{client_name}.key')

    if not os.path.exists(key_file):
        keys = RSA.generate(2048, os.urandom)
        with open(key_file, 'wb') as file:
            file.write(keys.export_key())
    else:
        with open(key_file, 'rb') as file:
            keys = RSA.import_key(file.read())

    CLIENT_LOGGER.debug('Ключи успешно загружены')

    database = ClientDB(client_name)

    try:
        transport = ClientTransport(server_address, server_port, database, client_name, client_password, keys)
    except ServerError as err:
        message = QMessageBox()
        message.critical(start_dialog, 'Ошибка сервера', err.text)
        exit(1)

    transport.setDaemon(True)
    transport.start()

    del start_dialog

    main_window = ClientMainWindow(database, transport, keys)
    main_window.make_connection(transport)
    main_window.setWindowTitle(f'Чат-программа - {client_name}')
    client_app.exec_()

    transport.transport_shutdown()
    transport.join()
