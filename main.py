from multiprocessing import Process
from threading import Thread

import checker_book
from bots import userIn


def chatting():
    while True:
        userIn.main()


def parsing():
    checker = checker_book.CheckerBook()
    checker.check_book()


def main():
    chat = Thread(target=chatting, args=(), name="Chatting")
    parse = Process(target=parsing, args=(), name="Parsing")

    chat.start()
    parse.start()

    chat.join()
    parse.join()


if __name__ == '__main__':
    main()
