"""
Unit-test программы-сервера
"""
import os
import sys
import unittest
sys.path.append(os.path.join(os.getcwd(), '..'))
from common.variables import RESPONSE, ERROR, ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME
from server import process_client_message


class TestServer(unittest.TestCase):
    """
    Класс теста программы-сервера
    """
    error_dict = {
        RESPONSE: 400,
        ERROR: 'Bad request'
    }
    success_dict = {RESPONSE: 200}

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_def_process_client_message_ok(self):
        """
        Тест обработки корректного запроса
        :return:
        """

        self.assertEqual(process_client_message({
            ACTION: PRESENCE,
            TIME: 1.1,
            USER: {
                ACCOUNT_NAME: 'Guest'
            }
        }), self.success_dict)

    def test_def_process_client_message_no_action(self):
        """
        Тест при отсутствии action в запросе
        :return:
        """

        self.assertEqual(process_client_message({
            TIME: 1.1,
            USER: {
                ACCOUNT_NAME: 'Guest'
            }
        }), self.error_dict)

    def test_def_process_client_message_wrong_action(self):
        """
        Тест при не верном действии
        :return:
        """

        self.assertEqual(process_client_message({
            ACTION: 'wrong action',
            TIME: 1.1,
            USER: {
                ACCOUNT_NAME: 'Guest'
            }
        }), self.error_dict)

    def test_def_process_client_message_no_time(self):
        """
        Тест при отсутствии времени в запросе
        :return:
        """

        self.assertEqual(process_client_message({
            ACTION: PRESENCE,
            USER: {
                ACCOUNT_NAME: 'Guest'
            }
        }), self.error_dict)

    def test_def_process_client_message_no_user(self):
        """
        Тест на отсутствие пользователя в запросе
        :return:
        """

        self.assertEqual(process_client_message({
            ACTION: PRESENCE,
            TIME: 1.1,
        }), self.error_dict)

    def test_def_process_client_message_wrong_user(self):
        """
        Тест на не корректного пользователя в запросе
        :return:
        """

        self.assertEqual(process_client_message({
            ACTION: PRESENCE,
            TIME: 1.1,
            USER: {
                ACCOUNT_NAME: 'Adam'
            }
        }), self.error_dict)


if __name__ == '__main__':
    unittest.main
