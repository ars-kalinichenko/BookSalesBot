from time import sleep

import IOC
from parsers import labirint, chitai_gorod


def add_book(url: str):
    if 'https://www.labirint.ru/books/' in url:
        lab = labirint.Labirint()
        lab.parsing(url)
        return lab.detail_book

    elif 'https://www.chitai-gorod.ru/catalog/book/' in url:
        ch_gorod = chitai_gorod.ChitaiGorod()
        ch_gorod.parsing(url)
        return ch_gorod.detail_book


def check_book():
    # some code
    sleep(2 ** 11)


def main():
    for url in IOC.queue_url:
        add_book(url)
    # add_book("https://www.chitai-gorod.ru/catalog/book/1188153/?watch_fromlist=cat_9072")


if __name__ == '__main__':
    main()
