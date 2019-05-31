import os.path
from urllib import request as urequest

import logger
from parsers import labirint, chitai_gorod, book24


class ParserManager:

    @staticmethod
    def shorten_link(link) -> str:
        """
        Shorten the link by '/?'. Applicable to book24 and chitai-gorod.
        If the link cannot be shortened, then the original is returned.
        """

        return link.split('/?')[0]

    def parsing_book(self, link: str) -> dict:
        """
        Parse the site and writes data about the book to the dictionary.

        If AttributeError (is an invalid reference), the cause is logged
         and the exception is passed to a higher level.
        """
        try:
            if 'https://www.labirint.ru/books/' in link:
                lab = labirint.Labirint()
                detail_book = lab.parsing(link)
                self.save_photo(detail_book)
                return detail_book.copy()

            elif 'https://www.chitai-gorod.ru/catalog/book/' in link:
                ch_gorod = chitai_gorod.ChitaiGorod()
                detail_book = ch_gorod.parsing(self.shorten_link(link))
                self.save_photo(detail_book)
                return detail_book.copy()

            elif 'https://book24.ru/product/' in link:
                book24_ = book24.Book24()
                detail_book = book24_.parsing(self.shorten_link(link))
                self.save_photo(detail_book)
                return detail_book.copy()

        except Exception as er:
            logger.show_error(system="parser_manager", error=repr(er))
            raise AttributeError

    @staticmethod
    def save_photo(book: dict):
        """
        Save the photo by reference and the name of the image from the dictionary
         with information about the book, if it does not exist.

        If the save folder does not exist, then it is created.
        """

        if not os.path.exists("images"):
            os.mkdir("images")

        image_name = f"images/{book['image_name']}"
        if "https://" in book['image_link']:
            if not os.path.isfile(image_name):
                with open(image_name, 'wb') as image:
                    image.write(urequest.urlopen(book['image_link']).read())
