import sys

from client.connect import connect
from utils.message import send_message, recv_message


def main():
    status = connect(sys.argv)
    while status:
        user_input = input('Ваше сообщение: ')
        send_message(status, 2, user_input)
        print(recv_message(status.recv(1048576)))


if __name__ == "__main__":
    main()
