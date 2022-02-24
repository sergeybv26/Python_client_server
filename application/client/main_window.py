"""
Главное окно
"""
import logging
import sys

from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor
from PyQt5.QtWidgets import QMainWindow, qApp, QMessageBox, QApplication
sys.path.append('../')
from client.dialog_add_contact import AddContactDialog
from client.dialog_del_contact import DelContactDialog
from client.main_window_ui import Ui_MainClientWindow
from errors import ServerError
import log.client_log_config

LOGGER = logging.getLogger('client')
select_dialog = None
remove_dialog = None


class ClientMainWindow(QMainWindow):
    def __init__(self, database, transport):
        super().__init__()
        self.database = database
        self.transport = transport

        self.ui = Ui_MainClientWindow()
        self.ui.setupUi(self)

        self.ui.menu_exit.triggered.connect(qApp.exit)

        self.ui.btn_send.clicked.connect(self.send_message)

        self.ui.btn_add_contact.clicked.connect(self.add_contact_window)
        self.ui.menu_add_contact.triggered.connect(self.add_contact_window)

        self.ui.btn_remove_contact.clicked.connect(self.delete_contact_window)
        self.ui.menu_del_contact.triggered.connect(self.delete_contact_window)

        self.contacts_model = None
        self.history_model = None
        self.messages = QMessageBox()
        self.current_chat = None
        self.ui.list_messages.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.list_messages.setWordWrap(True)

        self.ui.list_contacts.doubleClicked.connect(self.select_active_user)

        self.clients_list_update()
        self.set_disabled_input()
        self.show()

    def set_disabled_input(self):
        """
        Деактивирует поля ввода сообщения
        :return: None
        """
        self.ui.label_new_message.setText('Для выбора получателя дважды кликните на нем в окне контактов')
        self.ui.text_message.clear()
        if self.history_model:
            self.history_model.clear()

        self.ui.btn_clear.setDisabled(True)
        self.ui.btn_send.setDisabled(True)
        self.ui.text_message.setDisabled(True)

    def history_list_update(self):
        """
        Заполняет историю сообщений
        :return: None
        """
        list_messages = sorted(self.database.get_history(self.current_chat), key=lambda item: item[3])
        if not self.history_model:
            self.history_model = QStandardItemModel()
            self.ui.list_messages.setModel(self.history_model)

        self.history_model.clear()

        length = len(list_messages)
        start_index = 0
        if length > 20:
            start_index = length - 20

        for i in range(start_index, length):
            item = list_messages[i]
            if item[1] == 'in':
                msg = QStandardItem(f'Входящее сообщение от {item[3].replace(microsecond=0)}:\n{item[2]}')
                msg.setEditable(False)
                msg.setBackground(QBrush(QColor(255, 213, 213)))
                msg.setTextAlignment(Qt.AlignLeft)
                self.history_model.appendRow(msg)
            else:
                msg = QStandardItem(f'Исходящее сообщение от {item[3].replace(microsecond=0)}:\n{item[2]}')
                msg.setEditable(False)
                msg.setBackground(QBrush(QColor(204, 255, 204)))
                msg.setTextAlignment(Qt.AlignRight)
                self.history_model.appendRow(msg)
        self.ui.list_messages.scrollToBottom()

    def select_active_user(self):
        """
        Обрабатывает двойной клик по контакту
        :return: None
        """
        self.current_chat = self.ui.list_contacts.currentIndex().data()
        self.set_active_user()

    def set_active_user(self):
        """
        Устанавливает активного собеседника
        :return: None
        """
        self.ui.label_new_message.setText(f'Введите сообщение для {self.current_chat}:')
        self.ui.btn_clear.setDisabled(False)
        self.ui.btn_send.setDisabled(False)
        self.ui.text_message.setDisabled(False)

        self.history_list_update()

    def clients_list_update(self):
        """
        Обновляет список контактов
        :return: None
        """
        contacts_list = self.database.get_contacts()
        self.contacts_model = QStandardItemModel()
        for i in sorted(contacts_list):
            item = QStandardItem(i)
            item.setEditable(False)
            self.contacts_model.appendRow(item)
        self.ui.list_contacts.setModel(self.contacts_model)

    def add_contact_window(self):
        """
        Добавление контакта
        :return: None
        """
        global select_dialog
        select_dialog = AddContactDialog(self.transport, self.database)
        select_dialog.btn_ok.clicked.connect(lambda: self.add_contact_action(select_dialog))
        select_dialog.show()

    def add_contact_action(self, item):
        """
        Обрабатывает добавление контакта: сообщает серверу, обновляют таблицу и список контактов
        :param item: Экземпляр класса окна добавления пользователя
        :return: None
        """
        new_contact = item.selector.currentText()
        self.add_contact(new_contact)
        item.close()

    def add_contact(self, new_contact):
        """
        Добавляет контакт в БД
        :param new_contact: Добавляемый контакт
        :return: None
        """
        try:
            self.transport.add_contact(new_contact)
        except ServerError as err:
            self.messages.critical(self, 'Ошибка сервера', err.text)
        except OSError as err:
            if err.errno:
                self.messages.critical(self, 'Ошибка!', 'Потеряно соединение с сервером!')
                self.close()
            self.messages.critical(self, 'Ошибка', 'Таймаут соединения!')
        else:
            self.database.add_contact(new_contact)
            new_contact = QStandardItem(new_contact)
            new_contact.setEditable(False)
            self.contacts_model.appendRow(new_contact)
            LOGGER.info(f'Успешно добавлен контакт {new_contact}')
            self.messages.information(self, 'Успех', f'Контакт успешно добавлен.')

    def delete_contact_window(self):
        """
        Удаление контакта
        :return: None
        """
        global remove_dialog
        remove_dialog = DelContactDialog(self.database)
        remove_dialog.btn_ok.clicked.connect(lambda: self.delete_contact(remove_dialog))
        remove_dialog.show()

    def delete_contact(self, item):
        """
        Обрабатывает удаление контакта. Сообщает на сервер и обновляет таблицу контактов
        :param item: экземпляр класса окна удаления контакта
        :return: None
        """
        contact_name = item.selector.currentText()
        try:
            self.transport.remove_contact(contact_name)
        except ServerError as err:
            self.messages.critical(self, 'Ошибка сервера', err.text)
        except OSError as err:
            if err.errno:
                self.messages.critical(self, 'Ошибка!', 'Потеряно соединение с сервером!')
                self.close()
            self.messages.critical(self, 'Ошибка', 'Таймаут соединения!')
        else:
            self.database.del_contact(contact_name)
            self.clients_list_update()
            LOGGER.info(f'Успешно удален контакт {contact_name}')
            self.messages.information(self, 'Успех', f'Контакт успешно удален.')
            item.close()
            if contact_name == self.current_chat:
                self.current_chat = None
                self.set_disabled_input()

    def send_message(self):
        """
        Отправляет сообщение пользователю
        :return: None
        """
        message_text = self.ui.text_message.toPlainText()
        self.ui.text_message.clear()
        if not message_text:
            return
        try:
            self.transport.send_message(self.current_chat, message_text)
            LOGGER.info('Отправлено сообщение!!!')
        except ServerError as err:
            self.messages.critical(self, 'Ошибка сервера', err.text)
        except OSError as err:
            if err.errno:
                self.messages.critical(self, 'Ошибка!', 'Потеряно соединение с сервером!')
                self.close()
            self.messages.critical(self, 'Ошибка', 'Таймаут соединения!')
        except (ConnectionResetError, ConnectionAbortedError):
            self.messages.critical(self, 'Ошибка!', 'Потеряно соединение с сервером!')
            self.close()
        else:
            self.database.save_message(self.current_chat, 'out', message_text)
            LOGGER.debug(f'Отправлено сообщение для {self.current_chat}:\n{message_text}')
            self.history_list_update()

    @pyqtSlot(str)
    def message(self, sender):
        """
        Слот приема нового сообщения
        :param sender: контакт-отправитель
        :return: None
        """
        if sender == self.current_chat:
            self.history_list_update()
        else:
            if self.database.check_contact(sender):
                if self.messages.question(self, 'Новое сообщение',
                                          f'Получено новое сообщение от {sender}, открыть чат с ним?',
                                          QMessageBox.Yes, QMessageBox.No) == QMessageBox.Yes:
                    self.current_chat = sender
                    self.set_active_user()
            else:
                if self.messages.question(self, 'Новое сообщение',
                                          f'Получено новое сообщение от {sender}.\n'
                                          f'Данного пользователя нет в списке контактов.\n'
                                          f'Добавить в контакты и открыть чат с ним?',
                                          QMessageBox.Yes, QMessageBox.No) == QMessageBox.Yes:
                    self.add_contact(sender)
                    self.current_chat = sender
                    self.set_active_user()

    @pyqtSlot()
    def connection_lost(self):
        """
        Слот потери соединения. Выдает сообщение об ошибке и завершает работу приложения
        :return: None
        """
        self.messages.warning(self, 'Сбой соединения', 'Потеряно соединение с сервером.')
        self.close()

    def make_connection(self, trans_obj):
        """
        Создает соединение со слотами
        :param trans_obj: Экземпляр класса-транспорта клиента
        :return: None
        """
        trans_obj.new_message.connect(self.message)
        trans_obj.connection_lost.connect(self.connection_lost)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    from client_db import ClientDB
    database = ClientDB('test1')
    from transport import ClientTransport
    transport = ClientTransport('127.0.0.1', 7777, database, 'test1')
    window = ClientMainWindow(database, transport)
    sys.exit(app.exec_())
