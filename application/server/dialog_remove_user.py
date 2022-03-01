"""
Диалоговое окно удаления пользователя
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QPushButton


class DeleteUserDialog(QDialog):
    def __init__(self, database, server):
        super().__init__()
        self.database = database
        self.server_thread = server

        self.setWindowTitle('Удаление пользователя')
        self.setFixedSize(350, 120)
        self.setModal(True)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.selector_label = QLabel('Выберите пользователя для удаления:', self)
        self.selector_label.setFixedSize(200, 20)
        self.selector_label.move(10, 0)

        self.selector = QComboBox(self)
        self.selector.setFixedSize(200, 20)
        self.selector.move(10, 30)

        self.btn_ok = QPushButton('Удалить', self)
        self.btn_ok.setFixedSize(100, 30)
        self.btn_ok.move(230, 20)
        self.btn_ok.clicked.connect(self.remove_user)

        self.btn_cancel = QPushButton('Отмена', self)
        self.btn_cancel.setFixedSize(100, 30)
        self.btn_cancel.move(230, 60)
        self.btn_cancel.clicked.connect(self.close)

        self.all_users_fill()

    def all_users_fill(self):
        """
        Заполняет список пользователей
        :return: None
        """
        self.selector.addItems([user[0] for user in self.database.users_list()])

    def remove_user(self):
        """
        Обрабатывает удаление пользователя
        :return: None
        """
        self.database.remove_user(self.selector.currentText())
        if self.selector.currentText() in self.server_thread.names:
            sock = self.server_thread.names[self.selector.currentText()]
            del self.server_thread.names[self.selector.currentText()]
            self.server_thread.remove_client(sock)
        self.server_thread.service_update_lists()  # Рассылка клиентам о необходимости обновить справочники
        self.close()
