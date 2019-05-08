from time import sleep

from parsers import labirint, chitai_gorod


def add_book(url: str):
    if 'https://www.labirint.ru/books/' in url:
        lab = labirint.Labirint()
        lab.parsing(url)

    elif 'https://www.chitai-gorod.ru/catalog/book/' in url:
        ch_gorod = chitai_gorod.ChitaiGorod()
        ch_gorod.parsing(url)


def check_book():
    # some code
    sleep(2 ** 11)


def main():
    add_book("https://www.chitai-gorod.ru/catalog/book/1188153/?watch_fromlist=cat_9072")


if __name__ == '__main__':
    main()
