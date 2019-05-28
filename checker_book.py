import time

from bots import bot
from databases.database import Database
from parsers import parser_manager


class CheckerBook:
    @staticmethod
    def check_book():
        parser = parser_manager.ParserManager()
        bot_ = bot.Bot()
        while True:
            database = Database()
            books = database.get_books()

            for book in books:
                book_detail = parser.parsing_book(book['link'])

                if book_detail['price'] != book['price']:
                    database.change_price(book['link'], book_detail['price'])

                    if book_detail['price'] < book['price']:
                        sale = 100 - int(book_detail['price'] / book['price'] * 100)
                        for follower in book['followers']:
                            if database.check_service(follower):
                                bot_.send_notification(follower, book_detail, sale)

            database.__del__()
            time.sleep(1200)
