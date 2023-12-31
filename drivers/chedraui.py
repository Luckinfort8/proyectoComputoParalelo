import time
import platform

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


def chedraui_driver(items, best_item):
    chrome_path = '/usr/bin/google-chrome-stable' if platform.system() == 'Linux' else 'C:/Program Files/Google/Chrome/Application/chrome.exe'

    options = webdriver.ChromeOptions()
    options.binary_location = chrome_path

    total_info = dict()
    with webdriver.Chrome(options=options) as driver:
        item, bad_words, characteristics = items
        search_queries = [(f'{item} {charac}', restr) for charac, restr in characteristics]
        for search_query in search_queries:
            html = search_chedraui(driver, search_query[0])
            info = find_gallery_items(html, search_query[1], bad_words)
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


def search_chedraui(driver, query):
    driver.get("https://www.chedraui.com.mx")
    time.sleep(3)
    search_bar = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="¿Qué estás buscando?"]')
    search_bar.send_keys(query)
    search_bar.send_keys(Keys.RETURN)
    time.sleep(10)
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(10)
    html = driver.find_element(By.CSS_SELECTOR, 'body').get_attribute('outerHTML')
    return html


def find_gallery_items(html, restriction, bad_words):
    soup = BeautifulSoup(html, 'html.parser')
    prodoct_gallery = soup.find('div', {'id': 'gallery-layout-container'})
    product_list = prodoct_gallery.find_all('div', recursive=False)
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
        spam_general = product.select_one('span.vtex-product-price-1-x-currencyContainer')
        if spam_general is None:
            # print(f'No se encontro precio para {name}')
            continue
        text = []
        for spam in spam_general.find_all('span'):
            text.append(spam.text)
        price = ''.join(text)
        info.append((name, price, image, 'chedraui'))
    info.sort(key=lambda x: x[1])
    if len(info) > 0:
        return info[0]
    return None
