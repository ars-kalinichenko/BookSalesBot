import os.path
from time import sleep
from urllib import request as urequest

from parsers import labirint, chitai_gorod


def add_book(url: str):
    if 'https://www.labirint.ru/books/' in url:
        lab = labirint.Labirint()
        lab.parsing(url)
        detail_book = lab.detail_book
        save_photo(detail_book["image_link"], detail_book["image_name"])
        return lab.detail_book

    elif 'https://www.chitai-gorod.ru/catalog/book/' in url:
        ch_gorod = chitai_gorod.ChitaiGorod()
        ch_gorod.parsing(url)
        detail_book = ch_gorod.detail_book
        save_photo(detail_book["image_link"], detail_book["image_name"])
        return detail_book


def check_book():
    # some code
    sleep(2 ** 11)


def save_photo(url, name_image):
    if not os.path.exists("images"):
        os.mkdir("images")

    if not os.path.isfile(f'images/{name_image}'):
        with open(f'images/{name_image}', 'wb') as image:
            image.write(urequest.urlopen(url).read())
