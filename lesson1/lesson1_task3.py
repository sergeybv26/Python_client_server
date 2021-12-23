"""
3. Определить, какие из слов, поданных на вход программы, невозможно записать в байтовом типе.
Для проверки правильности работы кода используйте значения: «attribute», «класс», «функция», «type»
"""

STR_LIST = ['attribute', 'класс', 'функция', 'type']


def test_convert_string_to_byte(str_list):
    for elem in str_list:
        if not elem.isascii():
            print(f'Слово "{elem}" невозможно записать в байтовом типе')


test_convert_string_to_byte(STR_LIST)
