from socket import *

from utils.message import send_message, recv_message
from utils.settings import *
from utils.errors import errors
from utils.utility import get_args, sock_event


def disconnect(sock):
    sock.close()
    errors(0)


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
