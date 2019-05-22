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
        create_table_command = "CREATE TABLE followers(name varchar(100)," \
                               " chat_id integer NOT NULL, user_id integer NOT NULL," \
                               " subscriptions text ARRAY )"
        self.cursor.execute(create_table_command)

    def insert_book(self, info: dict):
        add_follower_command = f"UPDATE books SET followers = array_append(followers, {info['follower'][0]})" \
                         f" WHERE link = '{info['link']}' " \
                         f"and {info['follower'][0]} <> all (followers)"

        self.cursor.execute(add_follower_command)

        insert_book_command = f"INSERT INTO books(title, price, link, link_image, followers) " \
                              f"SELECT '{info['title']}', {info['price']}, '{info['link']}'," \
                              f" '{info['image_link']}', ARRAY{info['follower']} " \
                              f"where not exists(SELECT link FROM books WHERE link = '{info['link']}')"

        self.cursor.execute(insert_book_command)

    def __del__(self):
        self.cursor.close()
        self.connection.close()
