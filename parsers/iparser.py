from abc import ABC, abstractmethod

import requests


class IParser(ABC):
    link_from = None
    html = None

    def get_html(self, link):
        self.link_from = link
        self.html = requests.get(self.link_from).text

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
