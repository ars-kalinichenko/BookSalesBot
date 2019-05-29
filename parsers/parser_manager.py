import os.path
from urllib import request as urequest

import logger
from parsers import labirint, chitai_gorod, book24


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
                return detail_book.copy()

            elif 'https://www.chitai-gorod.ru/catalog/book/' in link:
                ch_gorod = chitai_gorod.ChitaiGorod()
                ch_gorod.parsing(self.shorten_link(link))
                detail_book = ch_gorod.detail_book
                self.save_photo(detail_book)
                return detail_book.copy()

            elif 'https://book24.ru/product/' in link:
                book24_ = book24.Book24()
                book24_.parsing(self.shorten_link(link))
                detail_book = book24_.detail_book
                self.save_photo(detail_book)
                return detail_book.copy()

        except AttributeError as ae:
            logger.show_error(system="parser_manager", error=repr(ae))
            raise AttributeError

    @staticmethod
    def save_photo(book: dict):
        if not os.path.exists("images"):
            os.mkdir("images")

        image_name = f"images/{book['image_name']}"

        if not os.path.isfile(image_name):
            with open(image_name, 'wb') as image:
                image.write(urequest.urlopen(book['image_link']).read())
