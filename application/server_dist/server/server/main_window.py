"""
Формирование главного окна сервера
"""
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QLabel, QTableView

from server.dialog_add_user import RegisterUser
from server.dialog_config import ConfigWindow
from server.dialog_remove_user import DeleteUserDialog
from server.stat_window import StatisticWindow

statistic_window = None
config_window = None
register_window = None
remove_window = None


class MainWindow(QMainWindow):
    """Класс - формирует главное окно приложения-сервера"""
    def __init__(self, database, server, config):
        super().__init__()
        self.database = database
        self.server_thread = server
        self.config = config

        self.exitAction = QAction('Выход', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.triggered.connect(qApp.quit)

        self.refresh_button = QAction('Обновить список', self)
        self.show_statistic_button = QAction('Статистика клиентов', self)
        self.config_button = QAction('Настройка сервера', self)
        self.register_button = QAction('Регистрация пользователя', self)
        self.remove_button = QAction('Удаление пользователя', self)

        self.statusBar()
        self.statusBar().showMessage('Server is working...')

        self.toolbar = self.addToolBar('MainBar')
        self.toolbar.addAction(self.exitAction)
        self.toolbar.addAction(self.refresh_button)
        self.toolbar.addAction(self.show_statistic_button)
        self.toolbar.addAction(self.config_button)
        self.toolbar.addAction(self.register_button)
        self.toolbar.addAction(self.remove_button)

        self.setFixedSize(800, 600)
        self.setWindowTitle('Messaging server')

        self.label = QLabel('Спмсок подключенных клиентов:', self)
        self.label.setFixedSize(240, 15)
        self.label.move(10, 25)

        self.active_clients_table = QTableView(self)
        self.active_clients_table.move(10, 45)
        self.active_clients_table.setFixedSize(780, 400)

        self.timer = QTimer()
        self.timer.timeout.connect(self.create_users_models)
        self.timer.start(1000)

        self.refresh_button.triggered.connect(self.create_users_models)
        self.show_statistic_button.triggered.connect(self.show_statistics)
        self.config_button.triggered.connect(self.server_config)
        self.register_button.triggered.connect(self.register_user)
        self.remove_button.triggered.connect(self.remove_user)

        self.show()

    def create_users_models(self):
        """
        Создает таблицу QModel для отображения в окне программы активных пользователей

        :return: None
        """
        users_list = self.database.active_users_list()
        table = QStandardItemModel()
        table.setHorizontalHeaderLabels(['Имя клиента', 'IP адрес', 'Порт', 'Время подключения'])
        for row in users_list:
            user, ip, port, time = row
            user = QStandardItem(user)
            user.setEditable(False)
            ip = QStandardItem(ip)
            ip.setEditable(False)
            port = QStandardItem(str(port))
            port.setEditable(False)
            time = QStandardItem(str(time.replace(microsecond=0)))
            time.setEditable(False)
            table.appendRow([user, ip, port, time])
        self.active_clients_table.setModel(table)
        self.active_clients_table.resizeColumnsToContents()
        self.active_clients_table.resizeRowsToContents()

    def show_statistics(self):
        """
        Формирует окно со статистикой клиентов

        :return: None
        """
        global statistic_window
        statistic_window = StatisticWindow(self.database)
        statistic_window.show()

    def server_config(self):
        """
        Формирует окно конфигурации сервера

        :return: None
        """
        global config_window
        config_window = ConfigWindow(self.config)

    def register_user(self):
        """
        Формирует окно регистрации пользователя

        :return: None
        """
        global register_window
        register_window = RegisterUser(self.database, self.server_thread)
        register_window.show()

    def remove_user(self):
        """
        Формирует окно удаление пользователя

        :return: None
        """
        global remove_window
        remove_window = DeleteUserDialog(self.database, self.server_thread)
        remove_window.show()


if __name__ == '__main__':
    pass
