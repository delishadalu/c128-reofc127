from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
import requests

browser = webdriver.Chrome('/Users/delishadavis/Desktop/python/chromedriver')
browser.get('https://exoplanets.nasa.gov/discovery/exoplanet-catalog/')
planets_data = []

time.sleep(10)


def scrape(hyperlink):
    try:
        page = requests.get(hyperlink)
        # BeautifulSoup Object
        soup = BeautifulSoup(page.content, "html.parser")
        temp_list=[]

        # Loop to find element using XPATH
        for tr_tag in soup.find_all("tr", attrs={"class", "fact_row"}):
            td_tags = tr_tag.find_all("td")

            

            for index, td_tag in enumerate(td_tags):

                try:
                    temp_list.append(td_tag.find_all(
                        "div", attrs={"class": "value"})[0].contents[0])
                
                except:
                    temp_list.append("")

            # add codes here...

        planets_data.append(temp_list)

        
    except:
        time.sleep(1)
        scrape(hyperlink)

df = pd.read_csv("/Users/delishadavis/Desktop/python/expoplanet.csv")

for index,row in df.iterrows():
    
    print(row["hyperlink"])
    scrape(row['hyperlink'])
    print(f"Data Scraping  completed")

# print(planets_data[0:10])
scrapped_data=[]
for row in planets_data:
    replaced = []
    for el in row:
        el = el.replace("\n", "")
        replaced.append(el)
    scrapped_data.append(replaced)

print(scrapped_data[0:10])
headers = ["planet_type", "discovery_date", "mass", "planet_radius",
           "orbital_radius", "orbital_period", "eccentricity", "detection_method"]
new_planet_df_1 = pd.DataFrame(scrapped_data, columns=headers)
new_planet_df_1.to_csv('new_scraped_data.csv')
