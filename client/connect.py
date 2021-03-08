
import json
from socket import *


from utils.settings import *
from utils.errors import errors
from utils.utility import get_args, sock_event, serialize_json, deserialize_json


def disconnect(sock):
    sock.close()
    errors(0)


def send_message(sock, flag, text=""):
    msg = serialize_json(flag, text)
    sock_event(sock.send(msg))
    if text == "quit":
        disconnect(sock)


def recv_message(sock):
    data = sock.recv(1048576)
    message = deserialize_json(data)
    return message


def connect(args):
    addr, port = get_args()
    sock = socket(AF_INET, SOCK_STREAM)
    sock_event(sock.connect((addr, port)))
    send_message(sock, 0)
    server_message = recv_message(sock)
    if server_message['status'] == message_flag[4]:
        print(f"{server_message['message']}")
        return sock
    else:
        errors(7)
