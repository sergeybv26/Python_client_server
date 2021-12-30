"""
2. Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах.
Написать скрипт, автоматизирующий его заполнение данными. Для этого:
Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item), количество (quantity),
цена (price), покупатель (buyer), дата (date). В это словаре параметров обязательно должны присутствовать
юникод-символы, отсутствующие в кодировке ASCII.
Функция должна предусматривать запись данных в виде словаря в файл orders.json.
При записи данных указать величину отступа в 4 пробельных символа;
Необходимо также установить возможность отображения символов юникода: ensure_ascii=False;
Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра.
"""
import json
from datetime import date


def write_order_to_json(item: str, quantity: int, price: float, buyer: str, date_order: str):
    """
    Записывает параметры заказа в json файл orders.json
    :param item: Наименование товара
    :param quantity: Количество товара
    :param price: Цена товара
    :param buyer: Покупатель
    :param date_order: Дата заказа
    :return: None
    """

    order_data = {
        'Товар': item,
        'Количество': quantity,
        'Цена': price,
        'Покупатель': buyer,
        'Дата': date_order
    }

    with open('orders.json', encoding='utf-8') as file:
        orders_data = json.load(file)

    orders_data['orders'].append(order_data)

    with open('orders.json', 'w', encoding='utf-8') as file:
        json.dump(orders_data, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    write_order_to_json('Компьютер', 5, 52100.0, 'Петров', f'{date.today()}')
    write_order_to_json('Принтер', 3, 22500.0, 'Петров', f'{date.today()}')

    with open('orders.json', encoding='utf-8') as f_n:
        print(f_n.read())
