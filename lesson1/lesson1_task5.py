"""
5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и
преобразовать результаты из байтовового в строковый (предварительно определив кодировку выводимых сообщений).
"""
import subprocess
from platform import system

import chardet

URLS_LIST = ['yandex.ru', 'youtube.com']


def subprocess_ping(url):
    parameter = '-n' if system().lower() == 'windows' else '-c'
    args = ['ping', parameter, '4', url]
    result = subprocess.Popen(args, stdout=subprocess.PIPE)
    for line in result.stdout:
        result = chardet.detect(line)
        line = line.decode(result['encoding']).encode('utf-8')
        print(line.decode('utf-8'))


subprocess_ping(URLS_LIST[0])
subprocess_ping(URLS_LIST[1])
