"""
Unit-test программы-клиента
"""
import os
import sys
import unittest

sys.path.append(os.path.join(os.getcwd(), '..'))

from client import create_presence, process_answ
from common.variables import TIME, ACTION, PRESENCE, USER, ACCOUNT_NAME, RESPONSE, ERROR


class TestClient(unittest.TestCase):
    """
    Класс теста программы-клиента
    """

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_def_create_presence(self):
        """
        Тест функции запроса на сервер
        :return:
        """

        request = create_presence()
        request[TIME] = 1.11

        self.assertEqual(request, {
            ACTION: PRESENCE,
            TIME: 1.11,
            USER: {
                ACCOUNT_NAME: 'Guest'
            }
        })

    def test_def_create_presence_instance(self):
        """
        Тест на корректность возвращаемого типа данных
        :return:
        """

        self.assertIsInstance(create_presence(), dict, 'Должна возвращать словарь')

    def test_process_answ_200(self):
        """
        Тест корректного разбора ответа 200
        :return:
        """
        self.assertEqual(process_answ({RESPONSE: 200}), '200 : OK')

    def test_process_answ_400(self):
        """
        Тест корректного разбора ответа 400
        :return:
        """
        self.assertEqual(process_answ({RESPONSE: 400, ERROR: 'Bad request'}), '400: Bad request')

    def test_process_answ_raise(self):
        """
        Тест не корректного разбора
        :return:
        """
        with self.assertRaises(ValueError):
            process_answ({})

    def test_process_answ_instance(self):
        """
        Тест типа возвращаемых данных
        :return:
        """
        self.assertIsInstance(process_answ({RESPONSE: 200}), str)

    def test_process_answ_key_error(self):
        """
        Тест на вызов ошибки при не корректных данных
        :return:
        """
        self.assertRaises(KeyError, process_answ, {RESPONSE: 300})


if __name__ == '__main__':
    unittest.main
