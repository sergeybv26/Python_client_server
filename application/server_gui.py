"""
Создание графического интерфейса для администратора сервера
"""
from PyQt5.QtGui import QStandardItemModel, QStandardItem


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
    history_list = database.
