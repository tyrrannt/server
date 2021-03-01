from socket import *
from contextlib import closing
import sys


import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', help='This parameter sets the port')
parser.add_argument('-a', '--addr', nargs='?', help='This parameter specifies the IP address to listen to')
port = parser.parse_args().port
addr = parser.parse_args().addr
if not port:
    print("Не указан порт")
    sys.exit()
if not addr:
    addr = ""

with socket(AF_INET, SOCK_STREAM) as sock:
    try:
        sock.bind((addr, int(port)))
    except ValueError:
        print("Не правильно указан порт")
        sys.exit()
    except gaierror:
        print("Не правильно указан адрес")
        sys.exit()
    except PermissionError:
        print("Ошибка доступа к порту. Порт уже занят, либо у вас недостаточно прав на его использование")
        sys.exit()

    sock.listen()
    while True:
        client, addr = sock.accept()
        with closing(client) as cl:
            data = cl.recv(1000000)
            print("Message: ", data.decode("ascii"), ", sent from client", addr)
            message = "Accepted"
            cl.send(message.encode("ascii"))
