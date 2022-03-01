"""
Создает хранилище сервера
"""

from datetime import datetime
from pprint import pprint

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class ServerDB:
    Base = declarative_base()

    class AllUsers(Base):
        __tablename__ = 'all_users'
        id = Column(Integer, primary_key=True)
        login = Column(String, unique=True)
        last_conn = Column(DateTime, default=datetime.now)
        password = Column(String)
        public_key = Column(Text, default=None)

        def __init__(self, login, pass_hash):
            self.login = login
            self.password = pass_hash

    class ActiveUsers(Base):
        __tablename__ = 'active_users'
        id = Column(Integer, primary_key=True)
        user = Column(Integer, ForeignKey('all_users.id'), unique=True)
        ip = Column(String)
        port = Column(Integer)
        time_conn = Column(DateTime)

        def __init__(self, user, ip, port, time_conn):
            self.user = user
            self.ip = ip
            self.port = port
            self.time_conn = time_conn

    class LoginHistory(Base):
        __tablename__ = 'login_history'
        id = Column(Integer, primary_key=True)
        user = Column(Integer, ForeignKey('all_users.id'))
        ip = Column(String)
        port = Column(Integer)
        last_conn = Column(DateTime)

        def __init__(self, user, ip, port, last_conn):
            self.user = user
            self.ip = ip
            self.port = port
            self.last_conn = last_conn

    class UsersContacts(Base):
        __tablename__ = 'contacts'
        id = Column(Integer, primary_key=True)
        user = Column(ForeignKey('all_users.id'))
        contact = Column(ForeignKey('all_users.id'))

        def __init__(self, user, contact):
            self.user = user
            self.contact = contact

    class UsersMessageStat(Base):
        __tablename__ = 'message_stat'
        id = Column(Integer, primary_key=True)
        user = Column(ForeignKey('all_users.id'))
        sent = Column(Integer)
        receive = Column(Integer)

        def __init__(self, user):
            self.user = user
            self.sent = 0
            self.receive = 0

    def __init__(self, path):
        self.engine = create_engine(f'sqlite:///{path}', echo=False, pool_recycle=7200,
                                    connect_args={'check_same_thread': False})
        self.Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        self.session.query(self.ActiveUsers).delete()
        self.session.commit()

    def user_login(self, username, ip_address, port, pubkey=None):
        """
        Записывает в базу факт входа пользователя. Обновляет публичный ключ пользователя, при его изменении
        :param username: имя пользователя
        :param ip_address: ip-адрес ПК, с которого подключается пользователь
        :param port: порт
        :param pubkey: публичный ключ
        :return: None
        """
        rez = self.session.query(self.AllUsers).filter_by(login=username)

        if rez.count():
            user = rez.first()
            user.last_conn = datetime.now()
            if user.public_key != pubkey:
                user.public_key = pubkey
        else:
            raise ValueError('Пользователь не зарегистрирован')

        new_active_user = self.ActiveUsers(user.id, ip_address, port, datetime.now())
        self.session.add(new_active_user)

        new_login_history = self.LoginHistory(user.id, ip_address, port, datetime.now())
        self.session.add(new_login_history)

        self.session.commit()

    def user_logout(self, username):
        """
        Фиксирует отключение пользователя. Удаляет пользователя из таблицы активных пользователей
        :param username: имя пользователя
        :return: None
        """
        user = self.session.query(self.AllUsers).filter_by(login=username).first()

        self.session.query(self.ActiveUsers).filter_by(user=user.id).delete()

        self.session.commit()

    def users_list(self):
        """
        Формирует список зарегистрированных пользователей и время их последнего входа
        :return: список кортежей (имя пользователя, время последнего входа)
        """
        query = self.session.query(
            self.AllUsers.login,
            self.AllUsers.last_conn
        )
        return query.all()

    def active_users_list(self):
        """
        Формирует список активных пользователей
        :return: список кортежей (имя пользователя, ip, порт, время входа)
        """
        query = self.session.query(
            self.AllUsers.login,
            self.ActiveUsers.ip,
            self.ActiveUsers.port,
            self.ActiveUsers.time_conn
        ).join(self.AllUsers)
        return query.all()

    def user_login_history(self, username=None):
        """
        Формирует историю входов пользователей. Если передано имя пользователя, то историю данного пользователя
        :param username: имя пользователя
        :return: список портежей (имя пользователя, ip, порт, время подключения)
        """
        query = self.session.query(
            self.AllUsers.login,
            self.LoginHistory.ip,
            self.LoginHistory.port,
            self.LoginHistory.last_conn
        ).join(self.AllUsers)

        if username:
            query = query.filter(self.AllUsers.login == username)

        return query.all()

    def process_message(self, sender, recipient):
        """
        Записывает в таблицу статистики факт передачи сообщения
        :param sender: имя отправителя
        :param recipient: имя получателя
        :return: None
        """
        sender = self.session.query(self.AllUsers).filter_by(login=sender).first().id
        recipient = self.session.query(self.AllUsers).filter_by(login=recipient).first().id
        sender_row = self.session.query(self.UsersMessageStat).filter_by(user=sender).first()
        sender_row.sent += 1

        recipient_row = self.session.query(self.UsersMessageStat).filter_by(user=recipient).first()
        recipient_row.receive += 1

        self.session.commit()

    def add_contact(self, user, contact):
        """
        Добавляет контакт для пользователя
        :param user: имя пользователя
        :param contact: имя добавляемого контакта
        :return: None
        """
        user = self.session.query(self.AllUsers).filter_by(login=user).first()
        contact = self.session.query(self.AllUsers).filter_by(login=contact).first()

        if not contact or self.session.query(self.UsersContacts).filter_by(user=user.id, contact=contact.id).count():
            return

        contact_row = self.UsersContacts(user.id, contact.id)
        self.session.add(contact_row)
        self.session.commit()

    def remove_contact(self, user, contact):
        """
        Удаляет контакт у пользователя
        :param user: имя пользователя
        :param contact: имя удаляемого контакта
        :return: None
        """
        user = self.session.query(self.AllUsers).filter_by(login=user).first()
        contact = self.session.query(self.AllUsers).filter_by(login=contact).first()

        if not contact:
            return

        self.session.query(self.UsersContacts).filter(
            self.UsersContacts.user == user.id,
            self.UsersContacts.contact == contact.id
        ).delete()

        self.session.commit()

    def get_contacts(self, username):
        """
        Формирует список контактов пользователя
        :param username: имя пользователя
        :return: список контактов
        """
        user = self.session.query(self.AllUsers).filter_by(login=username).first()

        query = self.session.query(self.UsersContacts, self.AllUsers.login). \
            filter_by(user=user.id). \
            join(self.AllUsers, self.UsersContacts.contact == self.AllUsers.id)

        return [contact[1] for contact in query.all()]

    def message_statistic(self):
        """
        Формирует статистику сообщений
        :return: Список кортежей (имя пользователя, время подключения, количество отправленных сообщений,
        количество принятых сообщений)
        """
        query = self.session.query(
            self.AllUsers.login,
            self.AllUsers.last_conn,
            self.UsersMessageStat.sent,
            self.UsersMessageStat.receive
        ).join(self.AllUsers)
        return query.all()

    def add_user(self, username, password):
        """
        Регистрация пользователя. Создает запись в таблице известных пользователей и таблице статистики сообщений
        :param username: имя пользователя
        :param password: хэш пароля
        :return: None
        """
        user_row = self.AllUsers(username, password)
        self.session.add(user_row)
        self.session.commit()

        statistic_row = self.UsersMessageStat(user_row.id)
        self.session.add(statistic_row)
        self.session.commit()

    def remove_user(self, username):
        """
        Удаление пользователя
        :param username: имя пользователя
        :return: None
        """
        user = self.session.query(self.AllUsers).filter_by(login=username).first()
        self.session.query(self.ActiveUsers).filter_by(user=user.id).delete()
        self.session.query(self.LoginHistory).filter_by(user=user.id).delete()
        self.session.query(self.UsersContacts).filter_by(user=user.id).delete()
        self.session.query(self.UsersContacts).filter_by(contact=user.id).delete()
        self.session.query(self.UsersMessageStat).filter_by(user=user.id).delete()
        self.session.query(self.AllUsers).filter_by(login=username).delete()
        self.session.commit()

    def get_password(self, username):
        """
        Получает из базы хэш пароля пользователя
        :param username: имя пользователя
        :return: хэш пароля
        """
        user = self.session.query(self.AllUsers).filter_by(login=username).first()
        return user.password

    def get_public_key(self, username):
        """
        Получает из базы публичный ключ пользователя
        :param username: имя пользователя
        :return: публичный ключ
        """
        user = self.session.query(self.AllUsers).filter_by(login=username).first()
        return user.public_key

    def check_user(self, username):
        """
        Проверяет существование пользователя
        :param username: имя пользователя
        :return: True - пользователь существует, False - пользователь не зарегистрирован
        """
        if self.session.query(self.AllUsers).filter_by(login=username).count():
            return True
        return False


if __name__ == '__main__':
    db = ServerDB('../server_base.db3')
    db.add_user('user-1', 'abcdef')
    db.add_user('user-2', 'abcdef')
    db.user_login('user-1', '192.168.1.2', 7777)
    db.user_login('user-2', '192.168.1.3', 7777)

    print(db.active_users_list())
    # print('-' * 50)
    #
    # db.user_logout('user-1')
    #
    # print(db.active_users_list())
    # print('-' * 50)
    #
    # db.user_logout('user-2')
    #
    # print(db.active_users_list())
    # print('-' * 50)
    # print(db.users_list())
    # print('-' * 50)
    # print(db.user_login_history())
    # print('-' * 50)
    # print(db.user_login_history('user-1'))
    # db.user_login('client-1', '192.168.1.2', 7778)
    # db.user_login('client-2', '192.168.1.3', 7779)
    # db.process_message('client-1', 'client-2')
    # pprint(db.message_statistic())
    #
    # db.user_login('client-3', '192.168.1.4', 7780)
    # db.add_contact('client-1', 'client-3')
    # print(db.get_contacts('client-1'))
    # db.remove_contact('client-1', 'client-3')
    # print(db.get_contacts('client-1'))
