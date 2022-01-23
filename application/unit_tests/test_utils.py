"""
Тесты утилит
"""
import argparse
import json
import sys
import unittest
from unittest.mock import patch

from common.utils import send_message, get_message, get_parameters
from common.variables import ENCODING, RESPONSE, ERROR, TIME, ACTION, PRESENCE, USER, ACCOUNT_NAME, DEFAULT_PORT, \
    DEFAULT_IP_ADDRESS


class TestSocket:
    """
    Класс для иммитации отправки и получения сообщений
    """

    def __init__(self, test_dict):
        self.test_dict = test_dict
        self.encoded_message = None
        self.received_message = None

    def send(self, message_to_send):
        """
        Тестовая функция отправки. Кодирует сообщение и сохраняет то, что будет отправлено в сокет
        :param message_to_send: Отправляемое сообщение
        :return:
        """

        json_test_message = json.dumps(self.test_dict)
        self.encoded_message = json_test_message.encode(ENCODING)
        self.received_message = message_to_send

    def recv(self, max_len):
        """
        Получение данных из сокета
        :return:
        """

        json_test_message = json.dumps(self.test_dict)
        return json_test_message.encode(ENCODING)


class TestUtils(unittest.TestCase):
    """
    Класс тестов утилит
    """

    error_dict = {
        RESPONSE: 400,
        ERROR: 'Bad request'
    }
    success_dict = {RESPONSE: 200}
    test_dict_send = {
        ACTION: PRESENCE,
        TIME: 1.1,
        USER: {
            ACCOUNT_NAME: 'Guest'
        }
    }

    def test_send_message(self):
        """
        Тест функции отправки
        :return:
        """

        test_socket = TestSocket(self.test_dict_send)
        send_message(test_socket, self.test_dict_send)

        self.assertEqual(test_socket.encoded_message, test_socket.received_message)

    def test_send_message_raise(self):
        """
        Тест ошибки при не словаре на входе
        :return:
        """

        test_socket = TestSocket(self.test_dict_send)
        self.assertRaises(TypeError, send_message, test_socket, 'message')

    def test_get_message_ok(self):
        """
        Тест приема сообщения с кодом 200
        :return:
        """

        test_sock_ok = TestSocket(self.success_dict)

        self.assertEqual(get_message(test_sock_ok), self.success_dict)

    def test_get_message_err(self):
        """
        Тест приема сообщения с кодом 400
        :return:
        """

        test_sock_err = TestSocket(self.error_dict)
        self.assertEqual(get_message(test_sock_err), self.error_dict)

    @patch.object(sys, 'argv', ['test_utils.py', '-a', '192.168.0.1'])
    def test_get_tcp_parameters_address(self):
        """
        Тест получения адреса из командной строки
        :return:
        """

        param = get_parameters()

        self.assertEqual(param.a, '192.168.0.1')

    @patch.object(sys, 'argv', ['test_utils.py', '-p', '8080'])
    def test_get_tcp_parameters_port(self):
        """
        Тест получения порта из командной строки
        :return:
        """

        param = get_parameters()

        self.assertEqual(param.p, '8080')

    def test_get_tcp_parameters_default_port(self):
        """
        Тест на установку порта по умолчанию
        :return:
        """

        param = get_parameters()
        self.assertEqual(param.p, DEFAULT_PORT)

    def test_get_tcp_parameters_default_address(self):
        """
        Тест получения адреса по умолчанию
        :return:
        """

        param = get_parameters()
        self.assertEqual(param.a, DEFAULT_IP_ADDRESS)

    def test_get_tcp_parameters_default_server_address(self):
        """
        Тест получения адреса по умолчанию для сервера
        :return:
        """

        param = get_parameters(True)
        self.assertEqual(param.a, '')

    def test_get_tcp_parameters_returned_type(self):
        """
        Тест проверка типа возвращаемых данных
        :return:
        """

        self.assertIsInstance(get_parameters(), argparse.Namespace)


if __name__ == '__main__':
    unittest.main
