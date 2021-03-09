import argparse
import getpass
import ipaddress
from socket import *
import json
from utils.errors import errors
from utils.settings import message_flag, encoding


def disconnect(sock):
    sock.close()
    errors(0)


def connect(args):
    addr, port = get_args()
    sock = socket(AF_INET, SOCK_STREAM)
    sock_event(sock.connect((addr, port)))
    send_message(sock, 0)
    server_message = recv_message(sock)
    if server_message['action'] == message_flag[4]:
        print(f"{server_message['message']}")
        return sock
    else:
        errors(7)


def send_message(sock, flag, text=""):
    msg = serialize_json(flag, text)
    sock_event(sock.send(msg))
    if text == "quit":
        disconnect(sock)



def recv_message(sock):
    data = sock.recv(1048576)
    message = deserialize_json(data)
    return message


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


def deserialize_json(data):
    message = json.loads(data.decode(encoding))
    return message


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
        errors(1)
    try:
        addr = parser.parse_args().addr
        if not addr:
            addr = "127.0.0.1"
        ipaddress.ip_address(addr)
    except ValueError:
        errors(2)
    return addr, port


def sock_event(func):
    try:
        func
    except ValueError:
        errors(1)
    except gaierror:
        errors(2)
    except PermissionError:
        errors(3)
    except ConnectionRefusedError:
        errors(4)
    except ConnectionResetError:
        errors(5)
    except ConnectionAbortedError:
        errors(6)


if __name__ == "__main__":
    pass
