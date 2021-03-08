from client.connect import *
import sys


def main():
    status = connect(sys.argv)
    while status:
        user_input = input('Ваше сообщение: ')
        send_message(status, 2, user_input)


if __name__ == "__main__":
    main()
