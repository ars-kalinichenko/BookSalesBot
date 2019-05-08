from bs4 import BeautifulSoup

from parsers.IParser import IParser


class ChitaiGorod(IParser):

    def get_price(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        prices = soup.select('div.product__price')
        prices = prices[0].get_text()
        return [int(s) for s in prices.split() if s.isdigit()][0]

    def get_title(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find(class_='product__header')
        title = title.find_all('h1')
        title = title[0].get_text()
        return title.strip()

    def get_image_link(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        img = soup.select("div.product__image img[src]")
        return img[0]["src"]

    def count_pages(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        pages = soup.find(class_='product__properties')

        for product_prop in pages.find_all(class_='product-prop'):
            for i in product_prop.find_all(class_='product-prop__title'):
                print(i.get_text() == 'Кол-во страниц')
        pages = pages.get_text()
        return [int(s) for s in pages.split() if s.isdigit()][0]

    def parsing(self, url):
        self.get_html(url)
        print(self.get_title(self.html))
        print(self.get_image_link(self.html))
        print(self.get_price(self.html))
        print(self.count_pages(self.html))
