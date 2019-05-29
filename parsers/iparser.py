from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup


class IParser(ABC):

    def get_soup(self, link) -> BeautifulSoup:
        html = requests.get(link).text
        return BeautifulSoup(html, 'html.parser')

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
    def get_image_name(self, image_link: str) -> str:
        pass
