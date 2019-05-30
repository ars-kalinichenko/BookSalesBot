import logger
from parsers.iparser import IParser


class Book24(IParser):
    """Parser for book24.ru"""
    detail_book = {}

    def get_price(self, soup):
        prices = soup.select('div.item-actions__prices')
        prices = prices[0].get_text()
        return [int(s) for s in prices.split() if s.isdigit()][0]

    def get_title(self, soup):
        title = soup.find(class_='item-detail__informations-box')
        title = title.find_all('h1')
        title = title[0].get_text()
        return title

    def get_image_link(self, soup):
        img = soup.find(class_='item-cover__item _preload')
        return img.select("img[src]")[0]['src']

    def get_image_name(self, image_link):
        im_extension = image_link.split(".")[-1]
        id_book = image_link.split('/')[4]
        return f"{id_book}.{im_extension}"

    def parsing(self, link):
        soup = self.get_soup(link)
        try:
            self.detail_book['link'] = link
            self.detail_book['title'] = self.get_title(soup)
            self.detail_book['price'] = self.get_price(soup)
            self.detail_book['image_link'] = self.get_image_link(soup)
            self.detail_book['image_name'] = self.get_image_name(self.detail_book['image_link'])
        except AttributeError as ae:
            logger.show_error(system="Book24", error=repr(ae))
            raise AttributeError
