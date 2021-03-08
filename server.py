import json
from socket import *
from contextlib import closing
from time import time
from utils.errors import errors
from utils.settings import encoding
from utils.utility import get_args, sock_event


addr, port = get_args()

with socket(AF_INET, SOCK_STREAM) as sock:
    sock_event(sock.bind((addr, port)))
    sock.listen()
    while True:
        client, addr = sock.accept()
        with closing(client) as cl:
            while True:
                data = cl.recv(1048576)
                client_message = json.loads(data.decode(encoding))
                try:
                    if client_message['action'] == "authenticate":
                        print(": ", client_message, ", sent from client", addr)
                        auth = {
                            "status": "Accepted",
                            "message": f"Hello {client_message['user']['username']}"
                        }
                        message = json.dumps(auth)
                        cl.send(message.encode(encoding))
                    if client_message['action'] == "message":
                        print(client_message, ", sent from client", addr)
                        if client_message["message"] == "quit":
                            break
                except KeyError:
                    print("Wrong action")
