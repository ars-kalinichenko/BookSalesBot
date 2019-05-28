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
    my_thread1 = Thread(target=chatting, args=(), name="Chatting")
    my_thread2 = Process(target=parsing, args=(), name="Parsing")

    my_thread1.start()
    my_thread2.start()

    my_thread1.join()
    my_thread2.join()


if __name__ == '__main__':
    main()
