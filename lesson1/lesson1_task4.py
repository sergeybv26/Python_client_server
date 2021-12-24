"""
4. Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового представления
в байтовое и выполнить обратное преобразование (используя методы encode и decode).
"""

STR_LIST = ['разработка', 'администрирование', 'protocol', 'standard']


def enc_dec_string(str_list):
    for elem in str_list:
        encoded = str.encode(elem, encoding='utf-8')
        decoded = bytes.decode(encoded, encoding='utf-8')
        print(f'Исходная строка: {elem}')
        print(f'Байтовое представление: {encoded}')
        print(f'Тип, при байтовом представлении: {type(encoded)}')
        print(f'Строка после обратного преобразования: {decoded}')
        print(f'Тип после обратного преобразования: {type(decoded)}')
        print('-' * 50)


enc_dec_string(STR_LIST)
