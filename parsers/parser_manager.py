import os.path
import time
from urllib import request as urequest

import logger
from bots import bot
from databases.database import Database
from parsers import labirint, chitai_gorod


class ParserManager:

    @staticmethod
    def shorten_link(link) -> str:
        return link.split('/?')[0]

    def parsing_book(self, link: str) -> dict:
        try:
            if 'https://www.labirint.ru/books/' in link:
                lab = labirint.Labirint()
                lab.parsing(link)
                detail_book = lab.detail_book
                self.save_photo(detail_book)
                return detail_book

            elif 'https://www.chitai-gorod.ru/catalog/book/' in link:
                ch_gorod = chitai_gorod.ChitaiGorod()

                ch_gorod.parsing(self.shorten_link(link))
                detail_book = ch_gorod.detail_book
                self.save_photo(detail_book)
                return detail_book

        except AttributeError as ae:
            logger.show_error(system="parser_manager", error=repr(ae))
            raise AttributeError

    def check_book(self):
        bot_ = bot.Bot()
        while True:
            database = Database()
            books = database.get_books()

            for book in books:
                book_detail = self.parsing_book(book['link'])

                if book_detail['price'] != book['price']:
                    database.change_price(book['link'], book_detail['price'])

                    if book_detail['price'] < book['price']:
                        sale = 100 - int(book_detail['price'] / book['price'] * 100)
                        for follower in book['followers']:
                            if database.check_service(follower):
                                self.save_photo(book_detail)
                                bot_.send_notification(follower, book_detail, sale)

            database.__del__()
            time.sleep(7200)

    @staticmethod
    def save_photo(book: dict):
        if not os.path.exists("images"):
            os.mkdir("images")

        image_name = f"images/{book['image_name']}"

        if not os.path.isfile(image_name):
            with open(image_name, 'wb') as image:
                image.write(urequest.urlopen(book['image_link']).read())
