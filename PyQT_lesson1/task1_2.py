"""
2. Написать функцию host_range_ping() для перебора ip-адресов из заданного диапазона.
Меняться должен только последний октет каждого адреса.
По результатам проверки должно выводиться соответствующее сообщение.
"""
from task1_1 import check_is_ip, host_ping


def host_range_ping(get_list=False):
    """
    Осуществляет проверку доступности ip-адресов для диапазона от стартого ip до введенного количества
    :param get_list: Флаг, указывающий на необходимость формирования спиков доступных и недоступных адресов
    :return: None
    """
    test_host_list = []

    while True:
        input_ip = input('Введите стартовый ip-адрес: ')
        try:
            ip_v4 = check_is_ip(input_ip)
        except Exception as err:
            print(f'{input_ip} - {err}. IP-адрес должен иметь вид: xxx.xxx.xxx.xxx')
            continue
        break

    ip_lower_octet = int(str(ip_v4).split('.')[-1])

    while True:
        quantity = int(input('Введите количество ip-адресов для проверки: '))
        if quantity + ip_lower_octet > 256:
            print(f'Ошибка! Количество ip-адресов не может превышать {256 - ip_lower_octet}')
            continue
        break

    for i in range(quantity):
        test_host_list.append(ip_v4 + i)

    result = host_ping(test_host_list, get_list)

    if get_list:
        return result


if __name__ == '__main__':
    host_range_ping()
