"""
2. Каждое из слов «class», «function», «method» записать в байтовом типе. Сделать это небходимо в автоматическом,
а не ручном режиме с помощью добавления литеры b к текстовому значению,
(т.е. ни в коем случае не используя методы encode и decode) и определить тип, содержимое и
длину соответствующих переменных.
"""
import ast

STR_LIST = ['class', 'function', 'method']


def convert_type(str_list):
    for elem in str_list:
        byte_as_string = f"b'{elem}'"
        result_str = ast.literal_eval(byte_as_string)
        print(f'Тип данных: {type(result_str)}')
        print(f'Содержимое после преобразования: {result_str}')
        print(f'Длина: {len(result_str)}')
    print('-' * 30)


convert_type(STR_LIST)
