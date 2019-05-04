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
#     prices = soup.select('div.buying-price')
#     prices = prices[0].get_text()
#     return [int(s) for s in prices.split() if s.isdigit()][0]
#
#
# def get_title(html):
#     soup = BeautifulSoup(html, 'html.parser')
#     title = soup.find(class_='prodtitle')
#     title = title.find_all('h1')
#     title = title[0].get_text()
#     return title.split(':')[1].strip()
#
#
# def get_image_link(html):
#     soup = BeautifulSoup(html, 'html.parser')
#     img = soup.find("div", {"id": "product-image"})
#     return img.select("img[src]")[0]['data-src']
#
#
# def count_pages(html):
#     soup = BeautifulSoup(html, 'html.parser')
#     title = soup.find(class_='pages2')
#     title = title.get_text()
#     return [int(s) for s in title.split() if s.isdigit()][0]
#
#
# def main():
#     base_url = 'https://www.labirint.ru/books/589212/'
#
#     print(get_title(get_html(base_url)))
#     print(get_image_link(get_html(base_url)))
#     print(get_price(get_html(base_url)))
#     print(count_pages(get_html(base_url)))
#
#
# if __name__ == '__main__':
#     main()
