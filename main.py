import threading

from bots import userIn
from parsers import parser_manager


def chatting():
    while True:
        userIn.main()


def parsing():
    parser_manager.check_book()


def main():
    my_thread1 = threading.Thread(target=chatting, args=())
    my_thread2 = threading.Thread(target=parsing, args=())

    my_thread1.start()
    my_thread2.start()

    my_thread1.join()
    my_thread2.join()


if __name__ == '__main__':
    main()
