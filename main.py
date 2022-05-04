import json

import nums_from_string
import requests as requests
from bs4 import BeautifulSoup

headers = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
}

def get_page(url):
    s = requests.Session()
    response = s.get(url=url, headers=headers)

    with open("page.html", 'w', encoding='utf-8') as file:
        file.write(response.text)

def collect_data(file_path):
    with open("page.html", 'r', encoding='utf-8') as file:
        src = file.read()
    soup = BeautifulSoup(src, 'lxml')

    result_list = []
    products_items = soup.find_all('div', class_='card-inner')
    for item in products_items:

        try:
            item_url = item.find('div', class_='product-title').find('a').get('href')
            item_url = 'https://www.viking-boots.ru/' + item_url
        except:
            item_url = None

        try:
            item_title = item.find('div', class_='product-title').text.strip()
        except:
            item_title = None

        try:
            old_price = item.find('span', class_='old-price').text
            old_price = nums_from_string.get_nums(old_price)[0]
        except:
            old_price = None

        try:
            new_price = item.find('span', class_='price').text
            new_price = nums_from_string.get_nums(new_price)[0]
        except:
            new_price = None

        try:
            discount_percent = item.find('span', class_='label label-discount').text.replace('до', '').strip()
        except:
            discount_percent = None

        result_list.append(
            {
               "link": item_url,
                "title": item_title,
                "old price": old_price,
                "new price": new_price,
                "discount_percent": discount_percent
            }
        )

    with open('result.json', 'w', encoding='utf-8') as file:
        json.dump(result_list, file, indent=4, ensure_ascii=False)



def main():
    get_page(url="https://www.viking-boots.ru/collection/rasprodazha?options%5B1585509%5D%5B%5D=12645404&order=price&page_size=96")
    collect_data(file_path=r'C:\Users\covsh\PycharmProjects\scraper viking-boots.ru\pagehtml')

if __name__ == '__main__':
    main()