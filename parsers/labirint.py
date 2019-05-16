from bs4 import BeautifulSoup

from parsers.iparser import IParser


class Labirint(IParser):
    """Parser for Labirint.ru"""
    detail_book = {}

    def get_price(self, html):
        """This method returns the current book price"""

        soup = BeautifulSoup(html, 'html.parser')
        prices = soup.select('div.buying-price')
        if len(prices) == 0:
            prices = soup.select('div.buying-pricenew')
        prices = prices[0].get_text()
        return [int(s) for s in prices.split() if s.isdigit()][0]

    def get_title(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find(class_='prodtitle')
        title = title.find_all('h1')
        title = title[0].get_text()
        if ':' not in title:
            return title.strip()
        return title.split(':')[1].strip()

    def get_image_link(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        img = soup.find("div", {"id": "product-image"})
        return img.select("img[src]")[0]['data-src']

    def parsing(self, url):
        self.get_html(url)
        self.detail_book['url'] = url
        self.detail_book['title'] = self.get_title(self.html)
        self.detail_book['price'] = self.get_price(self.html)
        self.detail_book['image'] = self.get_image_link(self.html)
