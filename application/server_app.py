"""
Программа-сервер. Объектно-ориентированный стиль
"""
import argparse
import configparser
import os.path
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from common.decos import log
from common.variables import SERVER_CONFIG, DEFAULT_PORT
from server.main_window import MainWindow
from server.server_core import Server
from server.server_db import ServerDB


@log
def get_server_parameters(default_address, default_port):
    """
    Получает параметры работы сервера из командной строки

    :param default_address: IP адрес по умолчанию, который слушает сервер
    :param default_port: порт по умолчанию
    :return: кортеж - параметры работы сервера (IP адрес, порт, флаг работы без графической оболочки)
    """
    parser_param = argparse.ArgumentParser()

    parser_param.add_argument('-a', default=default_address, nargs='?')
    parser_param.add_argument('-p', default=default_port, type=int, nargs='?')
    parser_param.add_argument('-n', '--no_gui', action='store_true')

    parameters = parser_param.parse_args(sys.argv[1:])
    listen_address = parameters.a
    listen_port = parameters.p
    flag_gui = parameters.no_gui

    return listen_address, listen_port, flag_gui


@log
def load_config():
    """
    Загружает конфигурацию сервера из ini файла, при наличии данных в файле. Иначе создает конфигурацию.

    :return: конфигурация сервера
    """
    config = configparser.ConfigParser()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config.read(f"{dir_path}/{SERVER_CONFIG}")

    if 'SETTINGS' in config:
        return config
    else:
        config.add_section('SETTINGS')
        config.set('SETTINGS', 'default_port', str(DEFAULT_PORT))
        config.set('SETTINGS', 'listen_address', '')
        config.set('SETTINGS', 'database_path', '')
        config.set('SETTINGS', 'database_file', 'server_base.db3')
        return config


def start_server_gui(_database, _server, _config):
    """
    Осуществляет запуск графической оболочки сервера. При закрытии окон останавливает обработчик сообщений

    :param _database: экземпляр класса обработчика базы данных
    :param _server: экземпляр класса сервера
    :param _config: конфигурация сервера
    :return: None
    """
    server_app = QApplication(sys.argv)
    server_app.setAttribute(Qt.AA_DisableWindowContextHelpButton)
    main_window = MainWindow(_database, _server, _config)
    server_app.exec_()
    _server.running = False


def main():
    """
    Основная функция сервера

    :return: None
    """
    config = load_config()

    listen_address, listen_port, flag_gui = get_server_parameters(config['SETTINGS']['listen_address'],
                                                                  config['SETTINGS']['default_port'])
    database = ServerDB(
        os.path.join(
            config['SETTINGS']['database_path'],
            config['SETTINGS']['database_file']
        )
    )

    server = Server(listen_address, listen_port, database)
    server.setDaemon(True)
    server.start()

    if flag_gui:
        while True:
            command = input('Введите gui для запуска графической оболочки, exit -  для завершения работы сервера: ')
            if command == 'exit':
                server.running = False
                server.join()
                break
            elif command == 'gui':
                start_server_gui(database, server, config)
                break
            else:
                print('Не корректная команда.')
    else:
        start_server_gui(database, server, config)


if __name__ == '__main__':
    main()
