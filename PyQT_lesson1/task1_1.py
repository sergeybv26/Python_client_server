"""
1. Написать функцию host_ping(), в которой с помощью утилиты ping будет проверяться доступность сетевых узлов.
Аргументом функции является список, в котором каждый сетевой узел должен быть представлен именем хоста или ip-адресом.
В функции необходимо перебирать ip-адреса и проверять их доступность с выводом соответствующего сообщения
(«Узел доступен», «Узел недоступен»).
При этом ip-адрес сетевого узла должен создаваться с помощью функции ip_address().
"""
import platform
from ipaddress import ip_address
from pprint import pprint
from subprocess import Popen, PIPE


def check_is_ip(ip_addr):
    """
    Выполняет проверку является ли аргумент ip адресом.
    :param ip_addr: ip-адрес для проверки
    :return: ip-адрес
    """
    try:
        ip_v4 = ip_address(ip_addr)
    except ValueError:
        raise Exception('Не является ip-адресом')

    return ip_v4


def host_ping(hosts_list, get_list=False):
    """
    Проверяет доступность сетевых узлов и выводит результат
    :param hosts_list: список сетевых узлов
    :param get_list: флаг - нужно ли возвращать список сетевых узлов с результатом теста
    :return: список словарей, если get_list = True
    """

    result = {'Доступные узлы': '', 'Недоступные узлы': ''}
    processes = []
    ping_param = '-n' if platform.system().lower() == 'windows' else '-c'

    for test_host in hosts_list:
        try:
            host = check_is_ip(test_host)
        except Exception as err:
            print(f'{test_host} - {err}. Принимается, что {test_host} является именем хоста')
            host = test_host
        args = ['ping', ping_param, '2', str(host)]

        process = Popen(args, stdout=PIPE)
        processes.append((host, process))

    for host, process in processes:
        if process.wait() == 0:
            result['Доступные узлы'] += f'{host}\n'
            if not get_list:
                print(f'Узел {host} - доступен')
        else:
            result['Недоступные узлы'] += f'{host}\n'
            if not get_list:
                print(f'Узел {host} - недоступен')
    if get_list:
        return result


if __name__ == '__main__':
    TEST_HOST_LIST = ['8.8.8.8', 'abc', 'ya.ru', 'google.com', 'kjks', '8.8.8.9']
    host_ping(TEST_HOST_LIST)
    res = host_ping(TEST_HOST_LIST, True)
    pprint(res)
