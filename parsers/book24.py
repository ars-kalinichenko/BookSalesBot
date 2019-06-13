import logger
from parsers.iparser import IParser


class Book24(IParser):
    """Parser for book24.ru"""

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
        detail_book = {}
        soup = self.get_soup(link)
        try:
            detail_book['link'] = link
            detail_book['title'] = self.get_title(soup)
            detail_book['price'] = self.get_price(soup)
            detail_book['image_link'] = self.get_image_link(soup)
            detail_book['image_name'] = self.get_image_name(detail_book['image_link'])
        except (AttributeError, IndexError) as ae:
            logger.show_error(system="Book24", error=repr(ae))
            raise AttributeError
        return detail_book
