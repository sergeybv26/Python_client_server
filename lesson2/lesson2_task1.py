"""
1. Задание на закрепление знаний по модулю CSV.
Написать скрипт, осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt, info_3.txt и
формирующий новый «отчетный» файл в формате CSV. Для этого:
Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными, их открытие и считывание данных.
В этой функции из считанных данных необходимо с помощью регулярных выражений извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения каждого параметра поместить в
соответствующий список. Должно получиться четыре списка — например, os_prod_list, os_name_list, os_code_list,
os_type_list. В этой же функции создать главный список для хранения данных отчета — например, main_data — и поместить
в него названия столбцов отчета в виде списка: «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения для этих столбцов также оформить в виде списка и поместить в файл main_data (также для каждого файла);
Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой функции реализовать получение данных
через вызов функции get_data(), а также сохранение подготовленных данных в соответствующий CSV-файл;
Проверить работу программы через вызов функции write_to_csv().
"""
import csv
import re

from chardet import detect


def read_file(filename: str):
    """
    Определяет кодировку файла и считывает из него данные в нужной кодировке
    :param filename: строка, содержащая имя файла
    :return: data
    """

    with open(filename, 'rb') as file:
        content = file.read()

    encoding = detect(content)['encoding']

    with open(filename, encoding=encoding) as file:
        data = file.read()

    return data


def get_data(filename_list: list):
    """
    Считывает данные из файлов и формирует итоговый список, содержащий списки с данными из файлов
    :param filename_list: список имен файлов для обработки
    :return: main_data
    """

    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    main_data = [['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']]

    os_prod_regex = re.compile(r'Изготовитель системы:\s*\S*')
    os_name_regex = re.compile(r'Windows\s*\S*')
    os_code_regex = re.compile(r'Код продукта:\s*\S*')
    os_type_regex = re.compile(r'Тип системы:\s*\S*')

    for filename in filename_list:
        data = read_file(filename)
        os_prod_list.append(os_prod_regex.findall(data)[0].split()[2])
        os_name_list.append(os_name_regex.findall(data)[0])
        os_code_list.append(os_code_regex.findall(data)[0].split()[2])
        os_type_list.append(os_type_regex.findall(data)[0].split()[2])
    main_data.append(os_prod_list)
    main_data.append(os_name_list)
    main_data.append(os_code_list)
    main_data.append(os_type_list)

    return main_data


def write_to_csv(file_csv: str):
    """
    Осуществляет вызов функции get_data() для получения данных и осуществляет запись этих данных в csv-файл.
    :param file_csv: ссылка на csv-файл
    :return: None
    """
    filename_list = ['info_1.txt', 'info_2.txt', 'info_3.txt']
    data = get_data(filename_list)
    temp_list = []

    with open(file_csv, 'w', encoding='utf-8', newline='') as file:
        file_writer = csv.writer(file)
        file_writer.writerow(data.pop(0))
        for elem_idx in range(len(data[0])):
            for data_idx in range(len(data)):
                temp_list.append(data[data_idx][elem_idx])
            file_writer.writerow(temp_list)
            temp_list = []


if __name__ == '__main__':
    write_to_csv('task1.csv')

    with open('task1.csv', encoding='utf-8') as f_n:
        LINES = csv.reader(f_n)
        for row in LINES:
            print(row)
