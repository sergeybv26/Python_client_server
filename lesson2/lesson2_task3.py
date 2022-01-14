"""
3. Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий сохранение данных в
файле YAML-формата. Для этого:
Подготовить данные для записи в виде словаря, в котором первому ключу соответствует список,
второму — целое число, третьему — вложенный словарь, где значение каждого ключа — это целое число с юникод-символом,
отсутствующим в кодировке ASCII (например, €);
Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml.
При этом обеспечить стилизацию файла с помощью параметра default_flow_style,
а также установить возможность работы с юникодом: allow_unicode = True;
Реализовать считывание данных из созданного файла и проверить, совпадают ли они с исходными.
"""
import yaml


def write_to_yaml(data: dict, filename: str):
    """
    Осуществляет запись словаря data в файл filename и последующую проверку записанных данных
    :param data: Словарь с данными для записи
    :param filename: Имя файла
    :return: None
    """

    with open(filename, 'w', encoding='utf-8') as file:
        yaml.dump(data, file, default_flow_style=False, allow_unicode = True)

    with open(filename, encoding='utf-8') as file:
        data_from_file = yaml.load(file, Loader=yaml.FullLoader)
        if data_from_file == data:
            print('Данные совпадают с исходными')
        else:
            print('Ошибка! Данные не совпадают')


if __name__ == '__main__':
    FIRST_DATA = ['data1', 3, 'Некоторые данные']
    SECOND_DATA = 45687
    THIRD_DATA = {
        '1₽': 'Данные',
        '2₽': 123,
        '3₽': 'data'
    }
    DATA = {
        'first': FIRST_DATA,
        'second': SECOND_DATA,
        'third': THIRD_DATA
    }

    write_to_yaml(DATA, 'task3.yaml')
