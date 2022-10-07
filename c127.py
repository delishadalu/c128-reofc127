from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd

browser = webdriver.Chrome('/Users/delishadavis/Desktop/python/chromedriver')
browser.get('https://exoplanets.nasa.gov/discovery/exoplanet-catalog/')
planets_data = []

time.sleep(10)


def scrape():
    for i in range(0, 10):
        print(f'Scrapping page {i+1} ...')

        # BeautifulSoup Object
        soup = BeautifulSoup(browser.page_source, "html.parser")

        # Loop to find element using XPATH
        for ul_tag in soup.find_all("ul", attrs={"class", "exoplanet"}):
            li_tags = ul_tag.find_all("li")

            temp_list = []

            for index, li_tag in enumerate(li_tags):

                if index == 0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")

            # add codes here...

            planets_data.append(temp_list)

        # Find all elements on the page and click to move to the next page
        browser.find_element(
            by=By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()


scrape()
headers = ["name", "light_years_from_earth", "planet_mass",
           "stellar_magnitude", "discovery_date"]

df = pd.DataFrame(planets_data, columns=headers)

df.to_csv('expoplanet.csv')
