from client.connect import disconnect
from utils.utility import deserialize_json, sock_event, serialize_json


def send_message(sock, flag, text=""):
    msg = serialize_json(flag, text)
    sock_event(sock.send(msg))
    if text == "quit":
        disconnect(sock)


def recv_message(sock):
    data = sock.recv(1048576)
    message = deserialize_json(data)
    return message
