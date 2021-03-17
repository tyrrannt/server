import argparse
import getpass
import ipaddress
import time
from socket import *
import json
from utils.errors import errors
from utils.settings import message_flag, encoding
from log import client_log_config, server_log_config
import inspect
import traceback

client_logger = client_log_config.logger
server_logger = server_log_config.logger


def log(func):
    def decorated(*args, **kwargs):
        res = func(*args, **kwargs)
        stack = inspect.stack()
        client_logger.info(
            f'<{time.ctime(time.time())}> Функция {func.__name__} вызвана из функции {stack[1].function}')
        return res

    return decorated


@log
def disconnect(sock):
    sock.close()
    client_logger.info('Завершение работы клиента.')
    errors(0)


@log
def connect(args):
    addr, port = get_args()
    sock = socket(AF_INET, SOCK_STREAM)
    try:
        sock_event(sock.connect((addr, port)))
    except ConnectionRefusedError:
        client_logger.info('Сервер не отвечает.')
        errors(4)
    send_message(sock, 0)
    server_message = recv_message(sock)
    if server_message['action'] == message_flag[4]:
        client_logger.info('Клиент успешно подключился к серверу.')
        print(f"{server_message['message']}")
        return sock
    else:
        client_logger.warning('Ошибка установки соединения.')
        errors(7)


@log
def send_message(sock, flag, text=""):
    msg = serialize_json(flag, text)
    try:
        sock_event(sock.send(msg))
    except ConnectionResetError:
        client_logger.critical('Сервер принудительно разорвал соединение.')
        errors(5)
    if text == "quit":
        disconnect(sock)


@log
def recv_message(sock):
    data = sock.recv(1048576)
    return deserialize_json(data)


@log
def serialize_json(flag, text):
    message = {
        "action": message_flag[int(flag)],
        "user": {
            "username": getpass.getuser(),
            "ip_address": gethostbyname(getfqdn())
        },
        "message": text
    }
    result = json.dumps(message)
    return result.encode(encoding)


@log
def deserialize_json(data):
    return json.loads(data.decode(encoding))


@log
def get_args():
    """
    Функция разбирать аргументы, передаваемые скрипту при его запуске из командной строки. Ищет в переданных аргументах
    IP адрес и порт. В случае  отсутствия аргументов, возвращает значения по умолчанию, адрес - 127.0.0.1, порт - 7777.
    Если же аргументы присутствуют, анализирует аргументы, и валидирует переданные значения, в случае ошибки вызывает
    функцию errors().
    :return: При успешной отработки функции, возвращает 2 переменные:
        addr: Содержит IP адрес. Тип - string
        port: Содержит порт. Тип - int
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', help='This parameter sets the port')
    parser.add_argument('-a', '--addr', nargs='?', help='This parameter specifies the IP address to listen to')
    try:
        if not parser.parse_args().port:
            port = 7777
        else:
            port = int(parser.parse_args().port)
    except ValueError:
        client_logger.info('Не правильно указан порт.')
        errors(1)
    try:
        addr = parser.parse_args().addr
        if not addr:
            addr = "127.0.0.1"
        ipaddress.ip_address(addr)
    except ValueError:
        client_logger.info('Не правильно указан адрес.')
        errors(2)
    return addr, port


@log
def sock_event(func):
    try:
        func
    except ValueError:
        client_logger.info('Не правильно указан порт.')
        errors(1)
    except gaierror:
        client_logger.info('Не правильно указан адрес.')
        errors(2)
    except PermissionError:
        client_logger.warning(
            'Ошибка доступа к порту. Порт уже занят, либо у вас недостаточно прав на его использование.')
        errors(3)
    except ConnectionRefusedError:
        client_logger.info('Сервер не отвечает.')
        errors(4)
    except ConnectionResetError:
        client_logger.critical('Сервер принудительно разорвал соединение.')
        errors(5)
    except ConnectionAbortedError:
        client_logger.critical('Сервер разорвал установленное подключение.')
        errors(6)


if __name__ == "__main__":
    pass
