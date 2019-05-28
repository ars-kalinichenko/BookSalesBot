from multiprocessing import Process
from threading import Thread

from bots import userIn
from parsers import parser_manager


def chatting():
    while True:
        userIn.main()


def parsing():
    parser = parser_manager.ParserManager()
    parser.check_book()


def main():
    my_thread1 = Thread(target=chatting, args=(), name="Chatting")
    my_thread2 = Process(target=parsing, args=(), name="Parsing")

    my_thread1.start()
    my_thread2.start()

    my_thread1.join()
    my_thread2.join()


if __name__ == '__main__':
    main()
