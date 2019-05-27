import os.path
import time
from urllib import request as urequest
from bots import bot
import logger
from databases.database import Database
from parsers import labirint, chitai_gorod


def shorten_link(link):
    return link.split('/?')[0]


def parsing_book(link: str):
    try:
        if 'https://www.labirint.ru/books/' in link:
            lab = labirint.Labirint()
            lab.parsing(link)
            detail_book = lab.detail_book
            save_photo(detail_book)
            return detail_book

        elif 'https://www.chitai-gorod.ru/catalog/book/' in link:
            ch_gorod = chitai_gorod.ChitaiGorod()

            ch_gorod.parsing(shorten_link(link))
            detail_book = ch_gorod.detail_book
            save_photo(detail_book)
            return detail_book

    except AttributeError as ae:
        logger.show_error(system="parser_manager", error=repr(ae))
        raise AttributeError


def check_book():
    bot_ = bot.Bot()
    while True:
        db = Database()
        books = db.get_books()
        for book in books:
            detail = parsing_book(book['link'])
            if detail['price'] != book['price']:

                db.change_price(book['link'], detail['price'])
                if detail['price'] < book['price']:
                    sale = 100 - int(detail['price'] / book['price'] * 100)
                    for follower in book['followers']:
                        if db.check_service(follower):
                            save_photo(detail)
                            bot_.send_notification(follower, book, sale)

        db.__del__()
        time.sleep(3000)


def save_photo(book: dict):
    if not os.path.exists("images"):
        os.mkdir("images")

    image_name = f"images/{book['image_name']}"

    if not os.path.isfile(image_name):
        with open(image_name, 'wb') as image:
            image.write(urequest.urlopen(book['image_link']).read())
