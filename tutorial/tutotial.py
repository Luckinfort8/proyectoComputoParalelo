from selenium import webdriver
from selenium.webdriver.support.ui import Select
import pandas as pd
import time

website = "https://www.adamchoi.co.uk/teamgoals/detailed"

# Descargar el chromedriver correspondiente a la versión de Chrome instalada y carmbiar
# la carpeta chromedriver-win64 por la que se descargó
path = "../chromedriver-win64/chromedriver.exe"

driver = webdriver.Chrome(path)
driver.get(website)

all_matches_button = driver.find_element_by_xpath('//label[@analytics-event="All matches"]')
all_matches_button.click()

# Esperar a que se cargue la página
time.sleep(4)

dropdown = Select(driver.find_element_by_id('country'))
dropdown.select_by_visible_text('Spain')

# Esperar a que se cargue la página
time.sleep(4)

matches = driver.find_elements_by_tag_name('tr')

date = []
home_team = []
score = []
away_team = []

for match in matches:
    date.append(match.find_element_by_xpath('./td[1]').text)
    home = match.find_element_by_xpath('./td[2]').text
    home_team.append(home)
    print(home)
    score.append(match.find_element_by_xpath('./td[3]').text)
    away_team.append(match.find_element_by_xpath('./td[4]').text)

driver.quit()

df = pd.DataFrame({'date': date, 'home_team': home_team, 'score': score, 'away_team': away_team})
df.to_csv('football_data.csv', index=False)
print(df)
