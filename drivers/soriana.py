import time
import platform

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import pandas as pd

def soriana_driver(items):
    website = "https://www.soriana.com"
    chrome_path = '/usr/bin/google-chrome-stable' if platform.system() == 'Linux' else 'C:/Program Files/Google/Chrome/Application/chrome.exe'

    options = webdriver.ChromeOptions()
    options.binary_location = chrome_path

    with webdriver.Chrome(options=options) as driver:
        total_info = []
        item, bad_words, characteristics = items
        search_queries = [(f'{item} {charac}', restr) for charac, restr in characteristics]
        for search_query in search_queries:
            for page_number in range(1, 9):  # Modify the range to scrape multiple pages
                page_url = f"https://www.soriana.com/electronica/equipos-de-computo/laptops/?&start=0&sz=25&pageNumber={page_number}&forceOldView=false&view=grid&cref=0&cgid=laptops"
                html = search_soriana(driver, page_url, search_query[0])
                info = find_gallery_items(html, search_query[1], bad_words)
                total_info.append((search_query, info))
    return total_info

def search_soriana(driver, page_url, query):
    driver.get(page_url)
    time.sleep(3)
    search_bar = driver.find_element(By.NAME, 'q')
    search_bar.clear()
    search_bar.send_keys(query)
    search_bar.send_keys(Keys.RETURN)
    time.sleep(10)
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(10)
    html = driver.find_element(By.CSS_SELECTOR, 'body').get_attribute('outerHTML')
    return html

# Rest of the code remains the same for finding and extracting product information

# Example of how to use the `soriana_driver` function
items = ("TV", ["Smart", "LED"], [("Full HD", "Full HD")])
result = soriana_driver(items)
print(result)


def find_gallery_items(html, restriction, bad_words):
    soup = BeautifulSoup(html, 'html.parser')
    product_list = soup.find_all('div', class_='col-4 col-sm-3 col-md-2-4 product-tile--wrapper')

    info = []
    for product in product_list:
        product_info = {}
        
        # Extract product name
        product_name = product.find('a', class_='plp-link')
        if product_name:
            product_info['name'] = product_name.text.strip()

        # Extract product brand
        product_brand = product.find('a', class_='product-tile--brand-link')
        if product_brand:
            product_info['brand'] = product_brand.text.strip()

        # Extract product image
        product_image = product.find('img', class_='tile-image')
        if product_image:
            product_info['image'] = product_image['data-src']

        # Extract product price
        product_price = product.find('span', class_='sales')
        if product_price:
            product_info['price'] = product_price.text.strip()

        # Check if product meets the restriction and bad words criteria
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

    return info