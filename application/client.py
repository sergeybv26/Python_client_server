"""
Программа-клиент. Объектно-ориентированный стиль
"""
import logging
import sys

from PyQt5.QtWidgets import QApplication

from client.client_db import ClientDB
from client.dialog_start import UserNameDialog
from client.main_window import ClientMainWindow
from client.transport import ClientTransport
from common.utils import get_parameters
from common.errors import ServerError
from common.decos import log

CLIENT_LOGGER = logging.getLogger('client')


@log
def check_client_parameters():
    """
    Выполняет проверку параметров клиента
    :return: Кортеж - параметры клиента
    """
    params = get_parameters()
    _server_address, _server_port, _client_name = params.a, params.p, params.name

    if not 1023 < _server_port < 65536:
        CLIENT_LOGGER.critical(f'Попытка запуска клиента с неподходящим номером порта '
                               f'{_server_port}. Допустимые номера порта: от 1024 до 65535. '
                               f'Клиент завершается.')
        sys.exit(1)

    return _server_address, _server_port, _client_name


if __name__ == '__main__':
    CLIENT_LOGGER.info('Запущено приложение')

    server_address, server_port, client_name = check_client_parameters()

    client_app = QApplication(sys.argv)

    if not client_name:
        start_dialog = UserNameDialog()
        client_app.exec_()
        if start_dialog.ok_pressed:
            client_name = start_dialog.client_name.text()
            del start_dialog
        else:
            exit(0)

    CLIENT_LOGGER.info(f'Запущен клиент с парамтрами: '
                       f'адрес сервера - {server_address}, '
                       f'порт - {server_port}, '
                       f'имя пользователя - {client_name}.')

    database = ClientDB(client_name)

    try:
        transport = ClientTransport(server_address, server_port, database, client_name)
    except ServerError as err:
        print(err.text)
        exit(1)

    transport.setDaemon(True)
    transport.start()

    main_window = ClientMainWindow(database, transport)
    main_window.make_connection(transport)
    main_window.setWindowTitle(f'Чат-программа - {client_name}')
    client_app.exec_()

    transport.transport_shutdown()
    transport.join()
