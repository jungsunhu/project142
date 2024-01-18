from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

# NASA Exoplanet URL
START_URL = "https://en.wikipedia.org/wiki/List_of_brown_dwarfs"
# Webdriver
browser = webdriver.Edge("msedgedriver.exe")
browser.get(START_URL)

time.sleep(10)

brown_dwarfs_data = []

def scrape_more_data(hyperlink):
    print(hyperlink)
    
    ## ADD CODE HERE ##
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content, 'html.parser')
        star_table = soup.find_all('table')
        # Retrieve data and append to list
        tempt_list = []
        table_rows = star_table[7].find_all('tr')
        for tr_tag in soup.find_all("tr",attrs={"class":"fact_row"}):
            td_tags = tr_tag.find_all("td")
            for td_tag in td_tags:
                try:
                    tempt_list.append(td_tag.find_all("div", attrs = {"class":"value"})[0].contents[0])
                except:
                    tempt_list.append
        
        brown_dwarfs_data.append(tempt_list)

    except:
        time.sleep(1)
        scrape_more_data(hyperlink)



brown_dwarfs_df_1 = pd.read_csv("updated_scraped_data.csv")

# Call method
for index, row in brown_dwarfs_df_1.iterrows():

     ## ADD CODE HERE ##
    print(row['hyperlink'])

     # Call scrape_more_data(<hyperlink>)
    scrape_more_data(row["hyperlink"])

    print(f"Data Scraping at hyperlink {index+1} completed")

print(brown_dwarfs_data)

# Remove '\n' character from the scraped data
scraped_data = []

for row in brown_dwarfs_data:
    replaced = []
    ## ADD CODE HERE ##
    for el in row:
        el = el.replace("\n", "")
        replaced.append(el)

    
    scraped_data.append(replaced)

print(scraped_data)

headers = ["planet_type","discovery_date", "mass", "planet_radius", "orbital_radius", "orbital_period", "eccentricity", "detection_method"]

brown_dwarfs_df_1 = pd.DataFrame(scraped_data,columns = headers)

# Convert to CSV
brown_dwarfs_df_1.to_csv('new_scraped_data.csv', index=True, index_label="id")
