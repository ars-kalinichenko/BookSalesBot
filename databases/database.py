import os

import psycopg2


class Database:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                f"dbname={os.environ.get('dbname')} \
                  user={os.environ.get('dbuser')} \
                  password={os.environ.get('dbpassword')} \
                  host={os.environ.get('dbhost')} \
                  port={os.environ.get('dbport')}")
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
        except Exception:
            print("Error ...")

    def create_table(self):
        create_table_command = "CREATE TABLE followers(id serial PRIMARY KEY, name varchar(100), chat_id integer NOT NULL, user_id integer NOT NULL,subscriptions  text ARRAY )"
        self.cursor.execute(create_table_command)

    def insert_book(self, info: dict):
        values = f"'{info['title']}', {info['price']}, '{info['url']}', '{info['image']}', ARRAY{info['follower']}"
        insert_command = f"INSERT INTO book(title, price, link, link_im, followers) VALUES({values})"
        self.cursor.execute(insert_command)

    def __del__(self):
        self.cursor.close()
        self.connection.close()
