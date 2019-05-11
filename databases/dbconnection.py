import psycopg2
import os


class DatabaseConnection:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                f"dbname={os.environ.get('dbname')} user={os.environ.get('dbuser')} password={os.environ.get('dbpassword')} host={os.environ.get('dbhost')} port={os.environ.get('dbport')}")
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
        except:
            print("Error ...")

    def create_table(self):
        create_table_command = "CREATE TABLE name_table(id serial PRIMARY KEY, title varchar(100), price integer NOT NULL, link varchar(256), link_im varchar(256), followers integer ARRAY)"
        self.cursor.execute(create_table_command)

    def insert_book(self):
        insert_command = "INSERT INTO book(title, price, link, link_im, followers) VALUES('Bill', 100, 'https', 'www', ARRAY[10000, 10000, 10000, 10000])"
        print(insert_command)
        self.cursor.execute(insert_command)

    def q_a(self):
        self.cursor.execute("SELECT * FROM book")
        books = self.cursor.fetchall()
        for book in books:
            print(book)
        self.cursor.close()
        self.connection.close()


if __name__ == '__main__':
    database_connection = DatabaseConnection()
    # database_connection.create_table()
    # database_connection.insert_book()
    database_connection.q_a()
