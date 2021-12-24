"""
6. Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», «сокет», «декоратор».
Проверить кодировку созданного файла (исходить из того, что вам априори неизвестна кодировка этого файла!).
Затем открыть этот файл и вывести его содержимое на печать.
ВАЖНО: файл должен быть открыт без ошибок вне зависимости от того, в какой кодировке он был создан!
"""
from chardet import detect

STR_LIST = ['сетевое программирование', 'сокет', 'декоратор']
FILENAME = 'test.txt'


def create_file(filename, str_list):
    with open(filename, 'w') as file:
        for line in str_list:
            file.write(line + '\n')


def read_file(filename):
    with open(filename, 'rb') as file:
        content = file.read()

    encoding = detect(content)['encoding']

    with open(filename, encoding=encoding) as file:
        for element in file:
            print(element, end='')


create_file(FILENAME, STR_LIST)
read_file(FILENAME)
