import psycopg2
from telebot.types import CallbackQuery
import os

class Database:
    def __init__(self):
        self.connection = psycopg2.connect(
            f"dbname={os.environ.get('dbname')} \
                  user={os.environ.get('dbuser')} \
                  password={os.environ.get('dbpassword')} \
                  host={os.environ.get('dbhost')} \
                  port={os.environ.get('dbport')}")
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()

    def start_following(self, chat_id: int):
        self.cursor.execute('UPDATE followers SET service = true WHERE chat_id = %s', (chat_id,))

    def stop_following(self, chat_id: int):
        self.cursor.execute('UPDATE followers SET service = false WHERE chat_id = %s', (chat_id,))

    def insert_book(self, info: dict, follower: list):
        self.cursor.execute(
            'INSERT INTO books(title, price, link, link_image, followers) SELECT %s, %s, %s, %s, %s'
            ' where not exists(SELECT link FROM books WHERE link = %s)',
            (info['title'], info['price'], info['link'], info['image_link'], follower, info['link']))

        self.cursor.execute(
            'UPDATE books SET followers = array_append(followers, %s) WHERE link = %s and %s <> all(followers)',
            (follower[0], info['link'], follower[0]))

    def insert_follower(self, link: list, call: CallbackQuery):
        self.cursor.execute(
            'INSERT INTO followers(chat_id, subscriptions) SELECT %s, %s '
            'where not exists(SELECT chat_id FROM followers WHERE chat_id = %s)',
            (call.message.chat.id, link, call.message.chat.id))

        self.cursor.execute(
            'UPDATE followers SET subscriptions = array_append(subscriptions, %s) '
            'WHERE chat_id = %s and %s <> all (subscriptions)',
            (link[0], call.message.chat.id, link[0]))

    def __del__(self):
        self.cursor.close()
        self.connection.close()
