import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import matplotlib.pyplot as plt
from multiprocessing import Process

list_prodcuts = [
    ('television', ['32 pulgadas', '55 pulgadas', '65 pulgadas', '75 pulgadas']),
    ('laptop', ['i3', 'i5', 'i7', 'i9']),

]