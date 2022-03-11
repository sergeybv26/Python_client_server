"""
Диалог выполнения регистрации пользователя
"""
import binascii
import hashlib

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QMessageBox, QApplication


class RegisterUser(QDialog):
    """Класс - формирует окно регистрации пользователя"""
    def __init__(self, database, server):
        super().__init__()
        self.database = database
        self.server_thread = server

        self.setWindowTitle('Регистрация пользователя')
        self.setFixedSize(175, 183)
        self.setModal(True)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.label_username = QLabel('Введите имя пользователя:', self)
        self.label_username.move(10, 10)
        self.label_username.setFixedSize(150, 15)

        self.username = QLineEdit(self)
        self.username.move(10, 30)
        self.username.setFixedSize(154, 20)

        self.label_password = QLabel('Введите пароль:', self)
        self.label_password.move(10, 55)
        self.label_password.setFixedSize(150, 15)

        self.password = QLineEdit(self)
        self.password.move(10, 75)
        self.password.setFixedSize(154, 20)
        self.password.setEchoMode(QLineEdit.Password)

        self.label_passwd_confirm = QLabel('Введите подтверждение:', self)
        self.label_passwd_confirm.move(10, 100)
        self.label_passwd_confirm.setFixedSize(150, 15)

        self.passwd_confirm = QLineEdit(self)
        self.passwd_confirm.move(10, 120)
        self.passwd_confirm.setFixedSize(154, 20)
        self.passwd_confirm.setEchoMode(QLineEdit.Password)

        self.btn_ok = QPushButton('Сохранить', self)
        self.btn_ok.move(10, 150)
        self.btn_ok.clicked.connect(self.save_data)

        self.btn_cancel = QPushButton('Выход', self)
        self.btn_cancel.move(90, 150)
        self.btn_cancel.clicked.connect(self.close)

        self.messages = QMessageBox()

        self.show()

    def save_data(self):
        """
        Проверяет правильность ввода и сохраняет в базу данных нового пользователя

        :return: None
        """
        if not self.username.text():
            self.messages.critical(self, 'Ошибка!', 'Не указано имя пользователя!')
            return
        elif self.password.text() != self.passwd_confirm.text():
            self.messages.critical(self, 'Ошибка!', 'Введенные пароли не совпадают!')
            return
        elif self.database.check_user(self.username.text()):
            self.messages.critical(self, 'Ошибка!', 'Пользователь уже существует!')
            return
        else:
            passwd_bytes = self.password.text().encode('utf-8')
            salt = self.username.text().lower().encode('utf-8')
            passwd_hash = hashlib.pbkdf2_hmac('sha512', passwd_bytes, salt, 100000)
            self.database.add_user(self.username.text(), binascii.hexlify(passwd_hash))
            self.messages.information(self, 'Успех!', 'Пользователь успешно зарегистрирован.')
            self.server_thread.service_update_lists()  # Рассылка клиентам о необходимости обновить справочники
            self.close()


if __name__ == '__main__':
    app = QApplication([])
    from server_db import ServerDB
    database = ServerDB('../server_base_test_db3')
    from server_core import Server
    server = Server('127.0.0.1', 7777, database)
    dialog = RegisterUser(database, server)
    app.exec_()
