import json
from socket import *
from contextlib import closing

from log import server_log_config
from utils.settings import encoding
from utils.utility import get_args, sock_event, send_message

addr, port = get_args()
server_logger = server_log_config.logger

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
                        msg = client_message + ", sent from client " + addr
                        server_logger.info(msg)
                        send_message(cl, 4, "Hello!")

                    if client_message['action'] == "message":
                        print(client_message, ", sent from client", addr)
                        if client_message["message"] == "quit":
                            server_logger.info('Клиент отключился')
                            break
                        send_message(cl, 5, client_message["message"])
                except KeyError:
                    print("Wrong action")
                    server_logger.warning('Неизвестное действие.')
