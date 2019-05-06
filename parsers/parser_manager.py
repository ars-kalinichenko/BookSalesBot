from parsers import Labirint, Chitai_Gorod


def check_state(url: str):
    if ('https://www.labirint.ru/books/' in url):
        try:
            Labirint.main()
        except EnvironmentError:
            pass
    elif ('https://www.chitai-gorod.ru/catalog/book/' in url):
        try:
            Chitai_Gorod.main()
        except EnvironmentError:
            pass
