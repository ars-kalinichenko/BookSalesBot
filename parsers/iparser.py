from abc import ABC, abstractmethod

import requests


class IParser(ABC):
    url_from = None
    html = None

    def get_html(self, url):
        self.url_from = url
        self.html = requests.get(self.url_from).text

    @abstractmethod
    def get_price(self, html: str) -> int:
        pass

    @abstractmethod
    def get_title(self, html: str) -> str:
        pass

    @abstractmethod
    def get_image_link(self, html: str) -> str:
        pass

    @abstractmethod
    def get_image_name(self, image_link, price: str) -> str:
        pass
