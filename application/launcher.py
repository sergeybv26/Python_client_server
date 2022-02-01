"""
Лаунчер для Windows
"""
import subprocess

PROCESS = []
CLIENT_SEND_QNT = 2
CLIENT_READ_QNT = 5

while True:
    ACTION = input('Выберите действие: q - выход, s - запустить сервер и клиенты, '
                   'x - закрыть все окна: ')

    if ACTION == 'q':
        while PROCESS:
            VICTIM = PROCESS.pop()
            VICTIM.kill()
        break
    elif ACTION == 's':
        PROCESS.append(subprocess.Popen('python server.py', creationflags=subprocess.CREATE_NEW_CONSOLE))
        for _ in range(CLIENT_SEND_QNT):
            PROCESS.append(subprocess.Popen('python client.py -m send',
                                            creationflags=subprocess.CREATE_NEW_CONSOLE))
        for _ in range(CLIENT_READ_QNT):
            PROCESS.append(subprocess.Popen('python client.py -m listen',
                                            creationflags=subprocess.CREATE_NEW_CONSOLE))
    elif ACTION == 'x':
        while PROCESS:
            VICTIM = PROCESS.pop()
            VICTIM.kill()
