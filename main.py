from multiprocessing import Process
from threading import Thread

import checker_book
from bots import userIn


def chatting():
    """User interaction."""

    while True:
        userIn.main()


def parsing():
    """Real-time tracking of discounts."""

    checker = checker_book.CheckerBook()
    checker.check_book()


def main():
    """Run these methods in parallel."""

    chat = Thread(target=chatting, args=(), name="Chatting")
    parse = Process(target=parsing, args=(), name="Parsing")

    chat.start()
    parse.start()

    chat.join()
    parse.join()


if __name__ == '__main__':
    main()
