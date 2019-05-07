from bs4 import BeautifulSoup

from parsers.IParser import IParser


class Labirint(IParser):
    """Parser for Labirint.ru"""

    def get_price(self, html):
        """This method return a price of book"""
        soup = BeautifulSoup(html, 'html.parser')
        prices = soup.select('div.buying-price')
        prices = prices[0].get_text()
        return [int(s) for s in prices.split() if s.isdigit()][0]

    def get_title(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find(class_='prodtitle')
        title = title.find_all('h1')
        title = title[0].get_text()
        return title.split(':')[1].strip()

    def get_image_link(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        img = soup.find("div", {"id": "product-image"})
        return img.select("img[src]")[0]['data-src']

    def count_pages(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        pages = soup.find(class_='pages2')
        pages = pages.get_text()
        return [int(s) for s in pages.split() if s.isdigit()][0]

    def parsing(self, url):
        self.get_html(url)
        print(self.get_title(self.html))
        print(self.get_image_link(self.html))
        print(self.get_price(self.html))
        print(self.count_pages(self.html))
