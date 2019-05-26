import os.path
from urllib import request as urequest

import logger
from parsers import labirint, chitai_gorod


def shorten_link(url):
    return url.split('/?')[0]


def add_book(url: str):
    try:
        if 'https://www.labirint.ru/books/' in url:
            lab = labirint.Labirint()
            lab.parsing(url)
            detail_book = lab.detail_book
            save_photo(detail_book)
            return detail_book

        elif 'https://www.chitai-gorod.ru/catalog/book/' in url:
            ch_gorod = chitai_gorod.ChitaiGorod()

            ch_gorod.parsing(shorten_link(url))
            detail_book = ch_gorod.detail_book
            save_photo(detail_book)
            return detail_book

    except AttributeError as ae:
        logger.show_error(system="parser_manager", error=repr(ae))
        raise AttributeError


def check_book():
    pass


def save_photo(book: dict):
    if not os.path.exists("images"):
        os.mkdir("images")

    image_name = f"images/{book['image_name']}"

    if not os.path.isfile(image_name):
        with open(image_name, 'wb') as image:
            image.write(urequest.urlopen(book['image_link']).read())
