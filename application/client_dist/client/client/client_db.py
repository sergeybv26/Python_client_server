"""
Создает хранилище клиента
"""
import os.path
from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class ClientDB:
    """
    Класс - осуществляет работу с базой данных клиента.
    """
    Base = declarative_base()

    class KnownUsers(Base):
        """
        Класс - создает таблицу известных пользователей
        """
        __tablename__ = 'known_users'
        id = Column(Integer, primary_key=True)
        username = Column(String)

        def __init__(self, username):
            self.username = username

    class MessageHistory(Base):
        """
        Класс - создает таблицу, хранящую историю сообщений
        """
        __tablename__ = 'message_history'
        id = Column(Integer, primary_key=True)
        contact = Column(String)
        direction = Column(String)
        message = Column(Text)
        date = Column(DateTime, default=datetime.now)

        def __init__(self, _contact, direction, message):
            self.contact = _contact
            self.direction = direction
            self.message = message

    class Contacts(Base):
        """
        Класс - создает таблицу для хранения контактов
        """
        __tablename__ = 'contacts'
        id = Column(Integer, primary_key=True)
        name = Column(String, unique=True)

        def __init__(self, _contact):
            self.name = _contact

    def __init__(self, name):
        path = os.path.dirname(os.path.realpath(__file__))
        filename = f'client_{name}.db3'
        self.engine = create_engine(f'sqlite:///{os.path.join(path, filename)}', echo=False, pool_recycle=7200,
                                    connect_args={'check_same_thread': False})
        self.Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        self.session.query(self.Contacts).delete()
        self.session.query(self.KnownUsers).delete()
        self.session.commit()

    def add_contact(self, _contact):
        """
        Добавляет контакт в базу данных

        :param _contact: имя контакта
        :return: None
        """
        if not self.session.query(self.Contacts).filter_by(name=_contact).count():
            contact_row = self.Contacts(_contact)
            self.session.add(contact_row)
            self.session.commit()

    def del_contact(self, _contact):
        """
        Удаляет контакт из базы данных

        :param _contact: имя контакта
        :return: None
        """
        self.session.query(self.Contacts).filter_by(name=_contact).delete()
        self.session.commit()

    def add_users(self, users_list):
        """
        Осуществляет заполнение таблицы известных пользователей

        :param users_list: список пользователей
        :return: None
        """
        for user in users_list:
            user_row = self.KnownUsers(user)
            self.session.add(user_row)
        self.session.commit()

    def save_message(self, _contact, direction, message):
        """
        Сохраняет сообщение в базе данных

        :param _contact: имя контакта
        :param direction: направляние: in или out
        :param message: текст сообщения
        :return: None
        """
        message_row = self.MessageHistory(_contact, direction, message)
        self.session.add(message_row)
        self.session.commit()

    def get_contacts(self):
        """
        Запрашивает из базы список всех контактов

        :return: Список контактов
        """
        return [_contact[0] for _contact in self.session.query(self.Contacts.name).all()]

    def get_users(self):
        """
        Запрашивает из базы список всех известных пользователей

        :return: список пользователей
        """
        return [user[0] for user in self.session.query(self.KnownUsers.username).all()]

    def check_user(self, user):
        """
        Осуществляет проверку существует ли пользователь в таблице известных пользователей

        :param user: имя пользователя
        :return: результат проверки - булево значение
        """
        if self.session.query(self.KnownUsers).filter_by(username=user).count():
            return True
        return False

    def check_contact(self, _contact):
        """
        Осуществляет проверку существует ли пользователь в таблице контактов

        :param _contact: имя контакта
        :return: результат проверки - булево значение
        """
        if self.session.query(self.Contacts).filter_by(name=_contact).count():
            return True
        return False

    def get_history(self, _contact):
        """
        Запрашивает в базе данных историю сообщений с пользователем

        :param _contact: имя пользователя
        :return: список кортежей (имя контакта, направление, текст сообщения, дата)
        """
        query = self.session.query(self.MessageHistory).filter_by(contact=_contact)

        return [(history_row.contact, history_row.direction, history_row.message,
                 history_row.date) for history_row in query.all()]

    def contacts_clear(self):
        """
        Очищает таблицу контактов

        :return: None
        """
        self.session.query(self.Contacts).delete()
        self.session.commit()


if __name__ == '__main__':
    db = ClientDB('client-1')
    for contact in ['client-3', 'client-4', 'client-5']:
        db.add_contact(contact)
    db.add_contact('client-4')
    db.add_users(['client-1', 'client-2', 'client-3', 'client-4', 'client-5', 'client-6'])
    db.save_message('client-1', 'in', f'Тестовое сообщение, отправленное {datetime.now()}')
    db.save_message('client-1', 'out', f'Тестовое сообщение, отправленное {datetime.now()}')

    print(db.get_contacts())
    print('-' * 100)
    print(db.get_users())
    print('-' * 100)
    print(db.check_user('client-5'))
    print('-' * 100)
    print(db.check_user('client-10'))
    print('-' * 100)
    print(db.get_history('client_1'))
    print('-' * 100)
    print(sorted(db.get_history('client-1'), key=lambda item: item[3]))
    print('-' * 100)
    print(db.check_contact('client-4'))
    print('-' * 100)
    print(db.get_history('client-2'))
    print('-' * 100)
    db.del_contact('client-5')
    print(db.get_contacts())
