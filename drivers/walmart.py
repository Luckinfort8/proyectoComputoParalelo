import time
import platform

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import pandas as pd

def walmart_driver(items):
    website = "https://www.walmart.com.mx"
    chrome_path = '/usr/bin/google-chrome-stable' if platform.system() == 'Linux' else 'C:/Program Files/Google/Chrome/Application/chrome.exe'

    options = webdriver.ChromeOptions()
    options.binary_location = chrome_path

    with webdriver.Chrome(options=options) as driver:
        total_info = []
        item, bad_words, characteristics = items
        search_queries = [(f'{item} {charac}', restr) for charac, restr in characteristics]
        for search_query in search_queries:
            html = search_walmart(driver, search_query[0])
            info = find_gallery_items(html, search_query[1], bad_words)
            total_info.append((search_query, info))
    return total_info

def search_walmart(driver, query):
    driver.get("https://www.walmart.com.mx")
    time.sleep(3)
    search_bar = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Buscar en Walmart"]')
    search_bar.send_keys(query)
    search_bar.send_keys(Keys.RETURN)
    time.sleep(10)
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(10)
    html = driver.find_element(By.CSS_SELECTOR, 'body').get_attribute('outerHTML')
    return html

def find_gallery_items(html, restriction, bad_words):
    soup = BeautifulSoup(html, 'html.parser')
    prodoct_gallery = soup.find('div', {'class': 'flex flex-wrap w-100 flex-grow-0 flex-shrink-0 ph2 pr0-xl pl4-xl mt0-xl'})
    product_list = prodoct_gallery.find_all('div', recursive=False)
    info = []
    for product in product_list:
        img = product.find('img')
        if img is None:
            continue
        name = img['alt']
        image = img['src']
        if not (name.find(restriction) != -1):
            continue
        breaking = False
        for bad_word in bad_words:
            if (name.lower().find(bad_word)) != -1:
                breaking = True
                break
        if breaking:
            continue
        spam_general = product.select_one('span.w_q67L')
        if spam_general is None:
            continue
        price = spam_general.text
        info.append((name, price, image, 'walmart'))
    return info