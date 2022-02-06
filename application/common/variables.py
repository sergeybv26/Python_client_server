"""
Настройки проекта. Константы
"""
import logging

DEFAULT_PORT = 7777
DEFAULT_IP_ADDRESS = '127.0.0.1'

MAX_CONNECTIONS = 5

MAX_PACKAGE_LENGTH = 1024

ENCODING = 'utf-8'
CLIENT_DEFAULT_MODE = 'listen'

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

# Константы логгирования
LOGGING_LEVEL = logging.DEBUG

# Константы ответов сервера

RESPONSE_400 = {
            RESPONSE: 400,
            ERROR: 'Bad request'
        }
