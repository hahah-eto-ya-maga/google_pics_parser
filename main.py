import os
import sys

import multiprocessing

import requests
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent

from time import time
import logging


headers = {'User-Agent': UserAgent().random}
def download_images(url):

    response = requests.get(url, headers=headers)
    soup = BS(response.text, 'html.parser')

    count = int(url.split('=')[-1]) + 1

    for element in soup.find_all('img'):
        try:
            imageUrl = element['src']
            if imageUrl.startswith('http'):
                imgData = requests.get(imageUrl, headers=headers).content
                with open(os.path.join('images', f"car_{count}.jpg"), 'wb') as file:
                    file.write(imgData)
                count += 1
        except Exception as e:
            print(logging.error(e))


if __name__ == "__main__":
    if not os.path.exists('images'):
        os.makedirs('images')

    numImages = 1000

    # ссылки для парсинга картинок
    urls = ['https://www.google.com/search?as_st=y&as_q=car+side+view&as_epq=&as_oq=car+side+view&as_eq=&imgar=&imgcolor=&imgtype=&cr=&as_sitesearch=&as_filetype=&tbs=&udm=2&tbm=isch&start=' + str(index) for index in range(0, numImages, 20)]

    for i in range(4):
        try:
            pools = int(input(f'Введите количество потоков (от 1 до 8 включительно{"!"*i}): '))
        except:
            print('Введите число!')
            continue
        if pools < 1 or pools > 8:
            if i == 3:
                input('Повторите попытку позже...')
                sys.exit(0)
            continue
        break

    start = time()

    print('Загрузка изображений...')

    with multiprocessing.Pool(pools) as process:
        process.map(download_images, urls)

    end = time() - start

    print('Изображения загружены в папку images внутри проекта!')
    print(f'Время загрузки: {str(end)[:5]} секунд.')
    input()
