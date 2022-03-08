"""
Стартовый дмалог клиента с вводом имени пользователя
"""
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, qApp, QApplication


class UserNameDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ok_pressed = False

        self.setWindowTitle('Привет!')
        self.setFixedSize(175, 135)

        self.label = QLabel('Введите имя пользователя:', self)
        self.label.move(10, 10)
        self.label.setFixedSize(150, 10)

        self.client_name = QLineEdit(self)
        self.client_name.setFixedSize(154, 20)
        self.client_name.move(10, 30)

        self.label_password = QLabel('Введите пароль:', self)
        self.label_password.move(10, 55)
        self.label_password.setFixedSize(150, 15)

        self.client_password = QLineEdit(self)
        self.client_password.setFixedSize(154, 20)
        self.client_password.move(10, 75)
        self.client_password.setEchoMode(QLineEdit.Password)

        self.btn_ok = QPushButton('Начать', self)
        self.btn_ok.move(10, 105)
        self.btn_ok.clicked.connect(self.click)

        self.btn_cancel = QPushButton('Выход', self)
        self.btn_cancel.move(90, 105)
        self.btn_cancel.clicked.connect(qApp.exit)

        self.show()

    def click(self):
        """
        Обрабатывает кнопку ОК. Если поле ввода не пустое устанавливает флаг и завершает приложение
        :return: None
        """
        if self.client_name.text():
            self.ok_pressed = True
            qApp.exit()


if __name__ == '__main__':
    app = QApplication([])
    dialog = UserNameDialog()
    app.exec_()
    print(dialog.ok_pressed)
