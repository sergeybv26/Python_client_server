"""
Лаунчер для Windows
"""
import subprocess

PROCESS = []
CLIENT_QNT = 3


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
        for i in range(1, CLIENT_QNT + 1):
            PROCESS.append(subprocess.Popen(f'python client.py -n client-{i}',
                                            creationflags=subprocess.CREATE_NEW_CONSOLE))

    elif ACTION == 'x':
        while PROCESS:
            VICTIM = PROCESS.pop()
            VICTIM.kill()
