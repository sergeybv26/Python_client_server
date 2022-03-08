"""
Дескриптор для описания порта сервера
"""
import logging
import log.server_log_config

SERVER_LOGGER = logging.getLogger('server')


class Port:
    def __set__(self, instance, value):
        if not 1023 < value < 65536:
            SERVER_LOGGER.critical(f'Попытка запуска сервера с неподходящим номером порта '
                                   f'{value}. Допустимые номера порта: от 1024 до 65535')
            exit(1)
        SERVER_LOGGER.info(f'Проверка номера порта прошла успешно. Порт сервера: {value}')
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name
