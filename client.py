from socket import *
import getpass
import sys

if len(sys.argv) == 3:
    sock = socket(AF_INET, SOCK_STREAM)
    try:
        sock.connect((sys.argv[1], int(sys.argv[2])))
    except ValueError:
        print("Не правильно указан порт")
        sys.exit()
    except gaierror:
        print("Не правильно указан адрес")
        sys.exit()
    message = getpass.getuser() + ';' + gethostbyname(getfqdn())
    sock.send(message.encode("ascii"))
    data = sock.recv(1000000)
    print("Answer: ", data.decode("ascii"), ", len ", len(data), "byte")
    sock.close()
else:
    print("Не верно переданы параметры сервера.")
