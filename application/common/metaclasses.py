"""
Метаклассы для проверки корректности сервера и клиентов
"""
import dis


class ServerMaker(type):
    """
    Метакласс для проверки корректности сервера
    """

    def __init__(cls, clsname, bases, clsdict):
        methods = []  # Методы, испульзуемые в функциях класса
        attrs = []  # Атрибуты, использующиеся в функциях класса
        for func in clsdict:
            try:
                ret = dis.get_instructions(clsdict[func])
            except TypeError:
                pass
            else:
                for instr in ret:
                    if instr.opname == 'LOAD_GLOBAL':
                        if instr.argval not in methods:
                            methods.append(instr.argval)
                    elif instr.opname == 'LOAD_ATTR':
                        if instr.argval not in attrs:
                            attrs.append(instr.argval)

        if 'connect' in methods:
            raise TypeError('Использование метода connect недопустимо в классе сервера')
        if not ('SOCK_STREAM' in attrs and 'AF_INET' in attrs):
            raise TypeError('Некорректная инициализация сокета')
        super().__init__(clsname, bases, clsdict)


class ClientMaker(type):
    """
    Метакласс для проверки корректности клиента
    """

    def __init__(cls, clsname, bases, clsdict):
        methods = []  # Методы, испульзуемые в функциях класса
        for func in clsdict:
            try:
                ret = dis.get_instructions(clsdict[func])
            except TypeError:
                pass
            else:
                for instr in ret:
                    if instr.opname == 'LOAD_GLOBAL':
                        if instr.argval not in methods:
                            methods.append(instr.argval)
        for command in ('accept', 'listen', 'socket'):
            if command in methods:
                raise TypeError('В классе клиента обнаружено использование запрещенного метода')
        if 'get_message' in methods or 'send_message' in methods:
            pass
        else:
            raise TypeError('Отсутствуют вызовы функций, работающих с сокетами')
        super().__init__(clsname, bases, clsdict)
