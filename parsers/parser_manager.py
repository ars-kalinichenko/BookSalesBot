from parsers import labirint, chitai_gorod


def add_book(url: str):
    if 'https://www.labirint.ru/books/' in url:
        lab = labirint.Labirint()
        try:
            lab.parsing(url)
        except EnvironmentError:
            pass
    elif 'https://www.chitai-gorod.ru/catalog/book/' in url:
        ch_gorod = chitai_gorod.ChitaiGorod()
        try:
            ch_gorod.parsing(url)
        except EnvironmentError:
            pass


def main():
    add_book("https://www.labirint.ru/books/694529/")


if __name__ == '__main__':
    main()
