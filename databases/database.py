import os

import psycopg2
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
        self.cursor = self.connection.cursor()

    def start_following(self, chat_id: int):
        start_command = f"UPDATE followers SET service = true " \
            f"WHERE chat_id = '{chat_id}'"
        self.cursor.execute(start_command)

    def stop_following(self, chat_id: int):
        stop_command = f"UPDATE followers SET service = false " \
            f"WHERE chat_id = '{chat_id}'"
        self.cursor.execute(stop_command)

    def insert_book(self, info: dict, follower: list):
        append_follower_command = f"UPDATE books SET followers = array_append(followers, {follower[0]})" \
            f" WHERE link = '{info['link']}' " \
            f"and {follower[0]} <> all (followers)"

        insert_book_command = f"INSERT INTO books(title, price, link, link_image, followers) " \
            f"SELECT '{info['title']}', {info['price']}, '{info['link']}'," \
            f" '{info['image_link']}', ARRAY{follower} " \
            f"where not exists(SELECT link FROM books WHERE link = '{info['link']}')"

        self.cursor.execute(insert_book_command)
        self.cursor.execute(append_follower_command)

    def insert_follower(self, link: list, call: CallbackQuery):
        insert_follower_command = f"INSERT INTO followers(chat_id, subscriptions) " \
            f"SELECT {call.message.chat.id}," \
            f"ARRAY{link} " \
            f"where not exists(SELECT chat_id FROM followers WHERE chat_id = '{call.message.chat.id}')"

        append_book = f"UPDATE followers SET subscriptions = array_append(subscriptions, '{link[0]}')" \
            f" WHERE chat_id = '{call.message.chat.id}' " \
            f"and '{link[0]}' <> all (subscriptions)"

        self.cursor.execute(insert_follower_command)
        self.cursor.execute(append_book)

    def __del__(self):
        self.cursor.close()
        self.connection.close()
