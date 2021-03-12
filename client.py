import sys
from utils.utility import send_message, recv_message, connect


def main():
    status = connect(sys.argv)
    while status:
        user_input = input('Ваше сообщение: ')
        send_message(status, 2, user_input)


if __name__ == "__main__":
    main()
