from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
import time
import platform


def get_data():
    print(platform.system())
    website = "https://www.adamchoi.co.uk/teamgoals/detailed"

    options = webdriver.ChromeOptions()
    options.binary_location = '/usr/bin/google-chrome-stable' if platform.system() == 'Linux' else 'C:/Program Files/Google/Chrome/Application/chrome.exe'

    driver = webdriver.Chrome(options)
    driver.get(website)

    all_matches_button = driver.find_element(By.XPATH, '//label[@analytics-event="All matches"]')
    all_matches_button.click()

    time.sleep(4)

    dropdown = Select(driver.find_element(By.ID, 'country'))
    dropdown.select_by_visible_text('Spain')

    time.sleep(4)

    matches = driver.find_elements(By.TAG_NAME, 'tr')

    date = []
    home_team = []
    score = []
    away_team = []

    for match in matches:
        date.append(match.find_element(By.XPATH, './td[1]').text)
        home = match.find_element(By.XPATH, './td[2]').text
        home_team.append(home)
        score.append(match.find_element(By.XPATH, './td[3]').text)
        away_team.append(match.find_element(By.XPATH, './td[4]').text)

    driver.quit()

    return date, home_team, score, away_team


def main():
    date, home_team, score, away_team = get_data()
    df = pd.DataFrame({'date': date, 'home_team': home_team, 'score': score, 'away_team': away_team})
    df.to_csv('football_data.csv', index=False)
    print(df)


if __name__ == '__main__':
    main()
