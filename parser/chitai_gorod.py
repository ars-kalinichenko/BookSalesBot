# import requests
# from bs4 import BeautifulSoup
#
#
# def get_html(url):
#     r = requests.get(url)
#     return r.text
#
#
# def get_price(html):
#     soup = BeautifulSoup(html, 'html.parser')
#     prices = soup.select('div.product__price')
#     prices = prices[0].get_text()
#     return [int(s) for s in prices.split() if s.isdigit()][0]
#
#
# def get_title(html):
#     soup = BeautifulSoup(html, 'html.parser')
#     title = soup.find(class_='product__header')
#     title = title.find_all('h1')
#     title = title[0].get_text()
#     return title.strip()
#
#
# def get_image_link(html):
#     soup = BeautifulSoup(html, 'html.parser')
#     img = soup.select("div.product__image img[src]")
#     return img[0]["src"]
#
#
# def count_pages(html):
#     soup = BeautifulSoup(html, 'html.parser')
#     title = soup.find(class_='product__properties')
#     title = title.find_all(class_='product-prop__value')[6]
#     title = title.get_text()
#     return [int(s) for s in title.split() if s.isdigit()][0]
#
#
# def main():
#     base_url = 'https://www.chitai-gorod.ru/catalog/book/1187950/?watch_fromlist=cat_9666'
#     print(get_title(get_html(base_url)))
#     print(get_image_link(get_html(base_url)))
#     print(get_price(get_html(base_url)))
#     print(count_pages(get_html(base_url)))
#
#
# if __name__ == '__main__':
#     main()
