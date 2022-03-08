"""
Формирует окно со статистикой пользователей
"""
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QDialog, QPushButton, QTableView


class StatisticWindow(QDialog):
    def __init__(self, database):
        super().__init__()
        self.database = database
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

        self.create_stat_model()

    def create_stat_model(self):
        """
        Реализует заполнение таблицы со статистикой сообщений
        :return: None
        """
        statistics_list = self.database.message_statistic()

        table = QStandardItemModel()
        table.setHorizontalHeaderLabels(
            ['Имя клиента', 'Последний раз входил', 'Сообщений отправлено', 'Сообщений получено']
        )
        for row in statistics_list:
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
        self.statistic_table.setModel(table)
        self.statistic_table.resizeColumnsToContents()
        self.statistic_table.resizeRowsToContents()
