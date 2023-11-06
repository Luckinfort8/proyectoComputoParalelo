import time
import platform

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import pandas as pd

def soriana_driver(items, best_item):
    chrome_path = '/usr/bin/google-chrome-stable' if platform.system() == 'Linux' else 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'

    options = webdriver.ChromeOptions()
    options.binary_location = chrome_path

    total_info = dict()
    with webdriver.Chrome(options=options) as driver:
        item, bad_words, characteristics = items
        search_queries = [(f'{item} {charac}', restr) for charac, restr in characteristics]
        for search_query in search_queries:
            html = search_soriana(driver, search_query[0])
            info = find_soriana_gallery_items(html, search_query[1], bad_words)
            if info is None:
                continue
            infodict = {
                'name': info[0],
                'price': info[1],
                'image': info[2],
                'store': info[3],
            }
            total_info[search_query[0]] = infodict
        best_item.add_item(total_info)

def search_soriana(driver, query):
    driver.get("https://www.soriana.com/")
    time.sleep(3)
    search_bar = driver.find_element(By.CSS_SELECTOR, 'input[id="searchBtnTrack"]')
    search_bar.clear()  # Limpiar cualquier texto existente en el campo de búsqueda
    search_bar.send_keys(query)
    search_bar.send_keys(Keys.RETURN)
    time.sleep(10)
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(10)
    html = driver.find_element(By.CSS_SELECTOR, 'body').get_attribute('outerHTML')
    return html

from bs4 import BeautifulSoup

def find_soriana_gallery_items(html, restriction, bad_words):
    soup = BeautifulSoup(html, 'html.parser')
    product_list = soup.find_all('div', class_='product-tile plp custom-product-tile position-relative js-product-card')

    info = []

    for product in product_list:
        product_info = {}

        # Extract product name
        product_name = product.find('a', class_='link plp-link font-primary--medium product-tile--link ellipsis-product-name font-size-16')
        if product_name:
            product_info['name'] = product_name.text.strip()

        # Extract product image
        product_image = product.find('img', class_='tile-image content-visibility-auto lazyload img-dimentions')
        if product_image:
            product_info['image'] = product_image['data-src']

        # Extract product brand
        product_brand = product.find('a', class_='product-tile--brand-link ellipsis-brand-name font-size-14')
        if product_brand:
            product_info['brand'] = product_brand.text.strip()

        # Extract product price
        product_price = product.find('span', class_='font-primary--bold font-size-14 cart-price price-plp price-not-found price-pdp')
        if product_price:
            product_info['price'] = product_price.text.strip()

        # Check if the product meets the restriction and bad words criteria
        if (
            'name' in product_info
            and 'price' in product_info
            and 'image' in product_info
            and product_info['name'].find(restriction) != -1
        ):
            breaking = False
            for bad_word in bad_words:
                if product_info['name'].lower().find(bad_word) != -1:
                    breaking = True
                    break
            if not breaking:
                info.append(product_info)

    info.sort(key=lambda x: x['price'])  # Sort by price (assuming 'price' is a numeric value)
    if len(info) > 0:
        return info[0]
    return None