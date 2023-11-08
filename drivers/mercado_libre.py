import time
import platform

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import pandas as pd

def ml_driver(items, best_item):
    chrome_path = '/usr/bin/google-chrome-stable' if platform.system() == 'Linux' else 'C:/Program Files/Google/Chrome/Application/chrome.exe'

    options = webdriver.ChromeOptions()
    options.binary_location = chrome_path

    total_info = dict()
    with webdriver.Chrome(options=options) as driver:
        item, bad_words, characteristics = items
        search_queries = [(f'{item} {charac}', restr) for charac, restr in characteristics]
        for search_query in search_queries:
            html = search_ml(driver, search_query[0])
            info = find_ml_gallery(html, search_query[1], bad_words)
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


def search_ml(driver, query):
    driver.get("https://www.mercadolibre.com.mx/")
    time.sleep(3)
    search_bar = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Buscar productos, marcas y más…"]')
    search_bar.clear()  # Limpiar cualquier texto existente en el campo de búsqueda
    search_bar.send_keys(query)
    search_bar.send_keys(Keys.RETURN)
    time.sleep(10)
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    html = driver.find_element(By.CSS_SELECTOR, 'body').get_attribute('outerHTML')
    return html


def find_ml_gallery(html, restriction, bad_words):
    soup = BeautifulSoup(html, 'html.parser')
    product_gallery = soup.find('ol', {'class': 'ui-search-layout ui-search-layout--stack'})
    product_list = product_gallery.find_all('li', recursive=False)
    info = []

    for product in product_list:
        img = product.find('img')
        if img is None:
            # print(f'No se encontro imagen para producto')
            continue
        name = img['alt']
        image = img['src']
        if image[:4] != 'http':
            continue
        if not (name.lower().find(restriction) != -1):
            # print(f'Restriccion {restriction} no encontrada en {name}')
            continue
        breaking = False
        for bad_word in bad_words:
            if (name.lower().find(bad_word)) != -1:
                # print(f'Bad word {bad_word} found in {name}')
                breaking = True
                break
        if breaking:
            continue
        spam_general = product.select_one('span.andes-money-amount__fraction')
        if spam_general is None:
            # print(f'No se encontro precio para {name}')
            continue
        price = f"${spam_general.text}.00"
        info.append((name, price, image, 'mercado libre'))

    info.sort(key=lambda x: x[1])  # Sort by price (assuming 'price' is a numeric value)
    if len(info) > 0:
        return info[0]
    return None