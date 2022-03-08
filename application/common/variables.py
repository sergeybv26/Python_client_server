"""
Настройки проекта. Константы
"""
import logging

DEFAULT_PORT = 7777
DEFAULT_IP_ADDRESS = '127.0.0.1'

MAX_CONNECTIONS = 5

MAX_PACKAGE_LENGTH = 10240

ENCODING = 'utf-8'
CLIENT_DEFAULT_MODE = 'listen'

SERVER_CONFIG = 'server/server.ini'

# Константы протокола JIM
ACCOUNT_NAME = 'account_name'
ACTION = 'action'
PRESENCE = 'presence'
PROBE = 'prоbe'
MSG = 'msg'
QUIT = 'quit'
AUTH = 'authenticate'
JOIN = 'join'
LEAVE = 'leave'
RESPONSE = 'response'
ERROR = 'error'
TIME = 'time'
USER = 'user'
MESSAGE = 'msg'
SENDER = 'from'
RECEIVER = 'to'
MESSAGE_TEXT = 'message'
GET_CONTACTS = 'get_contacts'
LIST_INFO = 'data_list'
REMOVE_CONTACT = 'remove'
ADD_CONTACT = 'add'
USERS_REQUEST = 'get_users'
DATA = 'bin'
PUBLIC_KEY = 'pubkey'
PUBLIC_KEY_REQUEST = 'pubkey_need'

# Константы логгирования
LOGGING_LEVEL = logging.DEBUG

# Константы ответов сервера

RESPONSE_202 = {
    RESPONSE: 202,
    LIST_INFO: None
}

RESPONSE_400 = {
            RESPONSE: 400,
            ERROR: 'Bad request'
        }

RESPONSE_205 = {
    RESPONSE: 205
}

RESPONSE_511 = {
    RESPONSE: 511,
    DATA: None
}
