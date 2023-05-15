import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import concurrent.futures
import time

start = time.perf_counter()

list_all_urls = []


def scraping(page_no:int, type_of_property:str):
    """
    Get all urls of all real-estate properties
    """
    page_number = f"{page_no}&orderBy=relevance"
    url_house = f"https://www.immoweb.be/en/search/{type_of_property}/for-sale?countries=BE&page={page_number}"
    with requests.Session() as session:
        url_text = session.get(url_house).text
    soup = BeautifulSoup(url_text, "html.parser")
    paragraphs = soup.find_all("h2", class_="card__title card--result__title")
    for paragraph in paragraphs:
        list_all_urls.append(paragraph.find("a", class_="card__title-link")["href"])
        print(paragraph.find("a", class_="card__title-link")["href"])
    return list_all_urls

#Multithreading for scraping all urls

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
    pages = range(1, 334)
    types = [
        "house-and-apartment",
        "new-real-estate-project-houses",
        "new-real-estate-project-apartments",
    ]
    pool.map(
        lambda x: scraping(*x),
        [
            (page_no, type_of_property)
            for page_no in pages
            for type_of_property in types
        ],
    )


def save(data):
    """
    Save all scraped urls
    """
    with open("output_urls.json", "w", encoding="utf-8") as output_urls:
        json.dump(data, output_urls, indent=2)


save(list_all_urls)

properties = []


def get_tables(url:list):

    """
    Scrape all tables of all real-estate properties.
    """

    url_text = requests.get(url)
    dfs = pd.read_html(url_text.text, index_col=0)
    dfs_concatenated = pd.concat(dfs)
    
    property = dfs_concatenated.T
    property[["url"]] = url
    property = property.set_index("url")
    property = property.loc[:, ~property.columns.duplicated()].copy()

    properties.append(property)
   
    return properties


#Multithreading for scraping all the tables of all urls

with concurrent.futures.ThreadPoolExecutor() as pool:
    pool.map(get_tables, list_all_urls)


#Concatenate all tables for each of the properties into one df

properties = pd.concat(properties)


#Finally saving all properties tables data as a csv 

properties.to_csv("immoweb_properties_data.csv")


end = time.perf_counter()
print(round((end - start), 2))
