from abc import ABC, abstractmethod

import requests


class IParser(ABC):
    url_from = None

    def set_url(self, url):
        self.url_from = url
        self.html = requests.get(self.url_from).text

    @abstractmethod
    def get_price(self, html):
        pass

    @abstractmethod
    def get_title(self, html):
        pass

    @abstractmethod
    def get_image_link(self, html):
        pass

    @abstractmethod
    def count_pages(self, html):
        pass
