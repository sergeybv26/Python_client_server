"""
Создает хранилище сервера
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class ServerDB:
    Base = declarative_base()

    class AllUsers(Base):
        __tablename__ = 'all_users'
        id = Column(Integer, primary_key=True)
        login = Column(String, unique=True)
        last_conn = Column(DateTime, default=datetime.now)

        def __init__(self, login):
            self.login = login

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

    class UsersContacts:
        __tablename__ = 'contacts'
        id = Column(Integer, primary_key=True)
        user = Column(ForeignKey('all_users.id'))
        contact = Column(ForeignKey('all_users.id'))

        def __init__(self, user, contact):
            self.user = user
            self.contact = contact

    class UsersMessageStat:
        __tablename__ = 'message_stat'
        id = Column(Integer, primary_key=True)
        user = Column(ForeignKey('all_users.id'))
        sent = Column(Integer)
        receive = Column(Integer)

        def __init__(self, user):
            self.user = user
            self.sent = 0
            self.receive = 0

    def __init__(self):
        self.engine = create_engine('sqlite:///server_base.db3', echo=False, pool_recycle=7200,
                                    connect_args={'check_same_thread': False})
        self.Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        self.session.query(self.ActiveUsers).delete()
        self.session.commit()

    def user_login(self, username, ip_address, port):
        rez = self.session.query(self.AllUsers).filter_by(login=username)

        if rez.count():
            user = rez.first()
            user.last_conn = datetime.now()
        else:
            user = self.AllUsers(username)
            self.session.add(user)
            self.session.commit()

        new_active_user = self.ActiveUsers(user.id, ip_address, port, datetime.now())
        self.session.add(new_active_user)

        new_login_history = self.LoginHistory(user.id, ip_address, port, datetime.now())
        self.session.add(new_login_history)

        self.session.commit()

    def user_logout(self, username):
        user = self.session.query(self.AllUsers).filter_by(login=username).first()

        self.session.query(self.ActiveUsers).filter_by(user=user.id).delete()

        self.session.commit()

    def users_list(self):
        query = self.session.query(
            self.AllUsers.login,
            self.AllUsers.last_conn
        )
        return query.all()

    def active_users_list(self):
        query = self.session.query(
            self.AllUsers.login,
            self.ActiveUsers.ip,
            self.ActiveUsers.port,
            self.ActiveUsers.time_conn
        ).join(self.AllUsers)
        return query.all()

    def user_login_history(self, username=None):
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
        sender = self.session.query(self.AllUsers).filter_by(login=sender).first().id
        recipient = self.session.query(self.AllUsers).filter_by(login=recipient).first().id

        sender_row = self.session.query(self.UsersMessageStat).filter_by(user=sender).first()
        sender_row.sent += 1
        # if sender_row.count():
        #     sender_row.first().sent += 1
        # else:
        #     sender_row = self.UsersMessageStat(sender)
        #     sender_row.sent += 1
        #     self.session.add(sender_row)

        recipient_row = self.session.query(self.UsersMessageStat).filter_by(user=recipient).first()
        # if recipient_row.count():
        recipient_row.receive += 1

        self.session.commit()

    def add_contact(self, user, contact):
        user = self.session.query(self.AllUsers).filter_by(login=user).first()
        contact = self.session.query(self.AllUsers).filter_by(login=contact).first()

        if not contact or self.session.query(self.UsersContacts).filter_by(user=user.id, contact=contact.id).count():
            return

        contact_row = self.UsersContacts(user.id, contact.id)
        self.session.add(contact_row)
        self.session.commit()

    def remove_contact(self, user, contact):
        user = self.session.query(self.AllUsers).filter_by(login=user).first()
        contact = self.session.query(self.AllUsers).filter_by(login=contact).first()

        if not contact:
            return

        print(self.session.query(self.UsersContacts).filter(
            self.UsersContacts.user == user.id,
            self.UsersContacts.contact == contact.id
        ).delete())

        self.session.commit()

    def get_contacts(self, username):
        user = self.session.query(self.AllUsers).filter_by(login=username).first()

        query = self.session.query()


if __name__ == '__main__':
    db = ServerDB()
    db.user_login('user-1', '192.168.1.2', 7777)
    db.user_login('user-2', '192.168.1.3', 7777)

    print(db.active_users_list())
    print('-' * 50)

    db.user_logout('user-1')

    print(db.active_users_list())
    print('-' * 50)

    db.user_logout('user-2')

    print(db.active_users_list())
    print('-' * 50)
    print(db.users_list())
    print('-' * 50)
    print(db.user_login_history())
    print('-' * 50)
    print(db.user_login_history('user-1'))
