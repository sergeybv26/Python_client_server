"""
Создание графического интерфейса для администратора сервера
"""
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QLabel, QTableView, QDialog, QPushButton, QLineEdit, \
    QFileDialog, QApplication


def gui_create_model(database):
    """
    Создает таблицу QModel для отображения в окне программы активных пользователей
    :param database: ссылка на класс базы данных
    :return: таблица
    """
    users_list = database.active_users_list()
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
    return table


def create_stat_model(database):
    """
    Реализует заполнение таблицы со статистикой сообщений
    :param database: ссылка на класс создания базы данных
    :return: таблица
    """
    history_list = database.message_statistic()

    table = QStandardItemModel()
    table.setHorizontalHeaderLabels(
        ['Имя клиента', 'Последний раз входил', 'Сообщений отправлено', 'Сообщений получено']
    )
    for row in history_list:
        user, last_conn, sent, receive = row
        user = QStandardItem(user)
        user.setEditable(False)
        last_conn = QStandardItem(str(last_conn.replace(microsecond=0)))
        last_conn.setEditable(False)
        sent = QStandardItem(str(sent))
        sent.setEditable(False)
        receive = QStandardItem(str(receive))
        receive.setEditable(False)
        table.appendRow([user, last_conn, sent, receive])
    return table


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.exitAction = QAction('Выход', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.triggered.connect(qApp.quit)

        self.refresh_button = QAction('Обновить список', self)
        self.show_statistic_button = QAction('Статистика клиентов', self)
        self.config_button = QAction('Настройка сервера', self)

        self.statusBar()

        self.toolbar = self.addToolBar('MainBar')
        self.toolbar.addAction(self.exitAction)
        self.toolbar.addAction(self.refresh_button)
        self.toolbar.addAction(self.show_statistic_button)
        self.toolbar.addAction(self.config_button)

        self.setFixedSize(800, 600)
        self.setWindowTitle('Messaging server')

        self.label = QLabel('Спмсок подключенных клиентов', self)
        self.label.setFixedSize(400, 15)
        self.label.move(10, 35)

        self.active_clients_table = QTableView(self)
        self.active_clients_table.move(10, 55)
        self.active_clients_table.setFixedSize(780, 400)

        self.show()


class StatisticWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Статистика клиентов')
        self.setFixedSize(600, 700)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.close_button = QPushButton('Закрыть', self)
        self.close_button.move(250, 650)
        self.close_button.clicked.connect(self.close)

        self.statistic_table = QTableView(self)
        self.statistic_table.move(10, 10)
        self.statistic_table.setFixedSize(580, 620)

        self.show()


class ConfigWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(365, 260)
        self.setWindowTitle('Настройки сервера')

        self.db_path_label = QLabel('Путь до файла базы данных: ', self)
        self.db_path_label.move(10, 10)
        self.db_path_label.setFixedSize(240, 15)

        self.db_path = QLineEdit(self)
        self.db_path.move(10, 30)
        self.db_path.setFixedSize(250, 20)
        self.db_path.setReadOnly(True)

        self.db_path_select = QPushButton('Обзор...', self)
        self.db_path_select.move(275, 28)

        def open_file_dialog():
            global dialog
            dialog = QFileDialog(self)
            path = dialog.getExistingDirectory()
            path = path.replace('/', '\\')
            self.db_path.insert(path)

        self.db_path_select.clicked.connect(open_file_dialog)

        self.db_file_label = QLabel('Имя файла базы данных: ', self)
        self.db_file_label.move(10, 68)
        self.db_file_label.setFixedSize(180, 15)

        self.db_file = QLineEdit(self)
        self.db_file.move(200, 66)
        self.db_file.setFixedSize(150, 20)

        self.port_label = QLabel('Номер порта для соединений: ', self)
        self.port_label.move(10, 108)
        self.port_label.setFixedSize(180, 15)

        self.port = QLineEdit(self)
        self.port.move(200, 108)
        self.port.setFixedSize(150, 20)

        self.ip_label = QLabel('С какого IP принимаем соединения: ', self)
        self.ip_label.move(10, 148)
        self.ip_label.setFixedSize(180, 15)

        self.ip_label_note = QLabel('оставьте это поле пустым, чтобы\nпринимать соединения с любых адресов.', self)
        self.ip_label_note.move(10, 168)
        self.ip_label_note.setFixedSize(500, 30)

        self.ip = QLineEdit(self)
        self.ip.move(200, 148)
        self.ip.setFixedSize(150, 20)

        self.save_button = QPushButton('Сохранить', self)
        self.save_button.move(190, 220)

        self.close_button = QPushButton('Закрыть', self)
        self.close_button.move(275, 220)
        self.close_button.clicked.connect(self.close)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.statusBar().showMessage('Server is running...')
    test_list = QStandardItemModel(main_window)
    test_list.setHorizontalHeaderLabels(['Имя Клиента', 'IP Адрес', 'Порт', 'Время подключения'])
    test_list.appendRow(
        [QStandardItem('test1'), QStandardItem('192.198.0.5'), QStandardItem('23544'), QStandardItem('16:20:34')]
    )
    test_list.appendRow(
        [QStandardItem('test2'), QStandardItem('192.198.0.8'), QStandardItem('33245'), QStandardItem('16:22:11')]
    )
    main_window.active_clients_table.setModel(test_list)
    main_window.active_clients_table.resizeColumnsToContents()
    app.exec_()
