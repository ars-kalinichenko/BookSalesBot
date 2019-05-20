import urllib
from time import sleep

import ioc
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


def save_photo(url, name_image):
    extension = url.split(".")[-1]
    with open(f'{name_image}.{extension}', 'wb') as image:
        image.write(urllib.request.urlopen(url).read())


def main():
    for url in ioc.queue_url:
        add_book(url)


if __name__ == '__main__':
    main()
