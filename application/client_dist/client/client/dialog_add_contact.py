"""
Создает диалог выбора контакта для добавления
"""
import logging
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QPushButton, QApplication
sys.path.append('../')
import log.client_log_config

LOGGER = logging.getLogger('client')


class AddContactDialog(QDialog):
    """Создает диалог выбора контакта для добавления"""
    def __init__(self, transport, database):
        super().__init__()
        self.transport = transport
        self.database = database

        self.setFixedSize(350, 120)
        self.setWindowTitle('Выберите контакт для добавления:')
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setModal(True)

        self.selector_label = QLabel('Выберите контакт для добавления:', self)
        self.selector_label.setFixedSize(200, 20)
        self.selector_label.move(10, 0)

        self.selector = QComboBox(self)
        self.selector.setFixedSize(200, 20)
        self.selector.move(10, 30)

        self.btn_refresh = QPushButton('Обновить список', self)
        self.btn_refresh.setFixedSize(100, 30)
        self.btn_refresh.move(60, 60)

        self.btn_ok = QPushButton('Добавить', self)
        self.btn_ok.setFixedSize(100, 30)
        self.btn_ok.move(230, 20)

        self.btn_cancel = QPushButton('Отмена', self)
        self.btn_cancel.setFixedSize(100, 30)
        self.btn_cancel.move(230, 60)
        self.btn_cancel.clicked.connect(self.close)

        self.possible_contacts_update()
        self.btn_refresh.clicked.connect(self.update_possible_users)

    def possible_contacts_update(self):
        """Заполнение списка возможных контактов разницей между всеми и уже добавленными пользователями"""
        self.selector.clear()

        contacts_list = set(self.database.get_contacts())
        users_list = set(self.database.get_users())

        users_list.remove(self.transport.username)

        self.selector.addItems(users_list - contacts_list)

    def update_possible_users(self):
        """Обновление списка известных пользователей (получает с сервера)"""
        try:
            self.transport.contacts_list_request()
        except OSError:
            LOGGER.error('Ошибка обновления списка пользователей с севера')
        else:
            LOGGER.debug('Выполнено обновление списка пользователей с сервера')
            self.possible_contacts_update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    from client_db import ClientDB

    database = ClientDB('client-1')
    from transport import ClientTransport

    transport = ClientTransport('127.0.0.1', 7777, database, 'client-1')
    window = AddContactDialog(transport, database)
    window.show()
    app.exec_()
