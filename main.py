import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import matplotlib.pyplot as plt
from multiprocessing import Process

list_prodcuts = [
    ('television', ['soporte'],
     [('32 pulgadas', '32'),
      ('55 pulgadas', '55'),
      ('65 pulgadas', '65'),
      ('75 pulgadas', '75'),
      ]),

]