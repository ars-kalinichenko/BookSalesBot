from bs4 import BeautifulSoup

from parsers.iparser import IParser


class ChitaiGorod(IParser):
    """Parser for Chitai_Gorod.ru"""
    detail_book = {}

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

    def get_image_name(self, image_link, price):
        im_extension = image_link.split(".")[-1]
        id_book = image_link.split('/')[5]
        return f"{price}{id_book}.{im_extension}"

    def parsing(self, url):
        self.get_html(url)
        self.detail_book['link'] = url
        self.detail_book['title'] = self.get_title(self.html)
        self.detail_book['price'] = self.get_price(self.html)
        self.detail_book['image_link'] = self.get_image_link(self.html)
        self.detail_book['image_name'] = self.get_image_name(self.detail_book['image_link'], self.detail_book['price'])
