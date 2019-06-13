import os

import psycopg2
from psycopg2.extras import DictCursor
from telebot.types import CallbackQuery


class Database:
    def __init__(self):
        self.connection = psycopg2.connect(
            f"dbname={os.environ.get('dbname')} \
                  user={os.environ.get('dbuser')} \
                  password={os.environ.get('dbpassword')} \
                  host={os.environ.get('dbhost')} \
                  port={os.environ.get('dbport')}")
        self.connection.autocommit = True
        self.cursor = self.connection.cursor(cursor_factory=DictCursor)

    def start_following(self, chat_id: int):
        """Change the value of user activity in the database to true."""

        self.cursor.execute('UPDATE followers SET service = true WHERE chat_id = %s', (chat_id,))

    def stop_following(self, chat_id: int):
        """Change the value of user activity in the database to false."""

        self.cursor.execute('UPDATE followers SET service = false WHERE chat_id = %s', (chat_id,))

    def insert_book(self, info: dict, follower: list):
        """Add a book to the list of books and to the list of subscriptions of the user, if it was not before."""

        self.cursor.execute(
            'INSERT INTO books(title, price, link, link_image, followers) SELECT %s, %s, %s, %s, %s'
            ' where not exists(SELECT link FROM books WHERE link = %s)',
            (info['title'], info['price'], info['link'], info['image_link'], follower, info['link']))

        self.cursor.execute(
            'UPDATE books SET followers = array_append(followers, %s) WHERE link = %s and %s <> all(followers)',
            (follower[0], info['link'], follower[0]))

    def insert_follower(self, link: list, call: CallbackQuery):
        """Add a user to the list of subscribers to the book and a list of users, if it was not before."""

        self.cursor.execute(
            'INSERT INTO followers(chat_id, subscriptions) SELECT %s, %s '
            'where not exists(SELECT chat_id FROM followers WHERE chat_id = %s)',
            (call.message.chat.id, link, call.message.chat.id))

        self.cursor.execute(
            'UPDATE followers SET subscriptions = array_append(subscriptions, %s) '
            'WHERE chat_id = %s and %s <> all (subscriptions)',
            (link[0], call.message.chat.id, link[0]))

    def get_subscriptions(self, chat_id: int) -> list:
        """
        Return a list of books to which the user is subscribed.
        If the list is empty, then return an empty list.
        """

        self.cursor.execute('SELECT subscriptions FROM followers WHERE chat_id = %s', (chat_id,))
        try:
            return self.cursor.fetchone()['subscriptions']
        except TypeError:
            return [None]

    def get_books(self) -> list:
        """Return a list of all references to books."""

        books_ = []
        self.cursor.execute('SELECT * FROM books')
        for row in self.cursor:
            books_.append({'id': row['id'],
                           'title': row['title'],
                           'price': row['price'],
                           'link': row['link'],
                           'link_image': row['link_image'],
                           'followers': row['followers']})
        return books_

    def check_service(self, chat_id: int) -> bool:
        """
        Check user activity in the database.
        If the user does not exist, then returns False.
        """

        self.cursor.execute('SELECT service FROM followers WHERE chat_id = %s', (chat_id,))
        try:
            return self.cursor.fetchone()['service']
        except TypeError:
            return False

    def change_price(self, link: str, price: int):
        """Change the price of a book in the database."""

        self.cursor.execute(
            'UPDATE books SET price = %s WHERE link = %s',
            (price, link))

    def delete_subscription(self, chat_id: int, link: str):
        """Remove a book by reference from a specific user's subscriptions."""

        self.cursor.execute("UPDATE books SET followers = array_remove(followers, %s) WHERE link = %s", (chat_id, link))
        self.cursor.execute("UPDATE followers SET subscriptions = array_remove(subscriptions, %s) WHERE chat_id = %s",
                            (link, chat_id))

    def delete_empty_subscriptions(self):
        """Removes books from which no one is subscribed."""

        self.cursor.execute("DELETE from books WHERE followers = '{}'")

    def __del__(self):
        self.cursor.close()
        self.connection.close()
