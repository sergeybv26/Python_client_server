"""
Создает хранилище клиента
"""
from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class ClientDB:
    Base = declarative_base()

    class KnownUsers(Base):
        __tablename__ = 'known_users'
        id = Column(Integer, primary_key=True)
        username = Column(String)

        def __init__(self, username):
            self.username = username

    class MessageHistory(Base):
        __tablename__ = 'message_history'
        id = Column(Integer, primary_key=True)
        from_user = Column(String)
        to_user = Column(String)
        message = Column(Text)
        date = Column(DateTime, default=datetime.now)

        def __init__(self, from_user, to_user, message):
            self.from_user = from_user
            self.to_user = to_user
            self.message = message

    class Contacts(Base):
        __tablename__ = 'contacts'
        id = Column(Integer, primary_key=True)
        name = Column(String, unique=True)

        def __init__(self, contact):
            self.name = contact

    def __init__(self, name):
        self.engine = create_engine(f'sqlite:///client_{name}.db3', echo=False, pool_recycle=7200,
                                    connect_args={'check_same_thread': False})
        self.Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        self.session.query(self.Contacts).delete()
        self.session.query(self.KnownUsers).delete()
        self.session.commit()

    def add_contact(self, contact):
        if not self.session.query(self.Contacts).filter_by(name=contact).count():
            contact_row = self.Contacts(contact)
            self.session.add(contact_row)
            self.session.commit()

    def del_contact(self, contact):
        self.session.query(self.Contacts).filter_by(name=contact).delete()
        self.session.commit()

    def add_users(self, users_list):
        for user in users_list:
            user_row = self.KnownUsers(user)
            self.session.add(user_row)
        self.session.commit()

    def save_message(self, from_user, to_user, message):
        message_row = self.MessageHistory(from_user, to_user, message)
        self.session.add(message_row)
        self.session.commit()

    def get_contacts(self):
        return [contact[0] for contact in self.session.query(self.Contacts.name).all()]

    def get_users(self):
        return [user[0] for user in self.session.query(self.KnownUsers.username).all()]

    def check_user(self, user):
        if self.session.query(self.KnownUsers).filter_by(username=user).count():
            return True
        return False

    def get_history(self, from_user=None, to_user=None):
        query = self.session.query(self.MessageHistory)
        if from_user:
            query = query.filter_by(from_user=from_user)
        if to_user:
            query = query.filter_by(to_user=to_user)
        return [(history_row.from_user, history_row.to_user, history_row.message,
                 history_row.date) for history_row in query.all()]


if __name__ == '__main__':
    db = ClientDB('client-1')
    for contact in ['client-3', 'client-4', 'client-5']:
        db.add_contact(contact)
    db.add_contact('client-4')
    db.add_users(['client-1', 'client-2', 'client-3', 'client-4', 'client-5'])
    db.save_message('client-1', 'client-4', f'Тестовое сообщение, отправленное {datetime.now()}')
    db.save_message('client-4', 'client-1', f'Тестовое сообщение, отправленное {datetime.now()}')

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
    print(db.get_history(to_user='client-1'))
    print('-' * 100)
    print(db.get_history())
    print('-' * 100)
    print(db.get_history('client-2'))
    print('-' * 100)
    db.del_contact('client-5')
    print(db.get_contacts())
