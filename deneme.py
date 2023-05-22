import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import concurrent.futures
import time

start = time.perf_counter()


class Scraper():
    def __init__(self):
        self.list_all_urls = []
        self.properties = []

    def scraping(self, page_no:int, type_of_property:str):

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
            self.list_all_urls.append(paragraph.find("a", class_="card__title-link")["href"])
            print(paragraph.find("a", class_="card__title-link")["href"])
        
        self.save()
        

    #Multithreading for scraping all urls

    def scrape_all_urls(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
            pages = range(1, 334)
            types = [
                "house-and-apartment",
                "new-real-estate-project-houses",
                "new-real-estate-project-apartments",
            ]
            pool.map(
                lambda x: self.scraping(*x),
                [
                    (page_no, type_of_property)
                    for page_no in pages
                    for type_of_property in types
                ],
            )


    def save(self):

        """
        Save all scraped urls
        """

        with open("output_urls.json", "w", encoding="utf-8") as output_urls:
            json.dump(self.list_all_urls, output_urls, indent=2)

    def get_tables(self, url:list):

        """
        Scrape all tables of all real-estate properties.
        """
        
        session = requests.Session()
        url_text = session.get(url)
        dfs = pd.read_html(url_text.text, index_col=0)
        dfs_concatenated = pd.concat(dfs)

        property = dfs_concatenated.T
        property[["url"]] = url
        property = property.set_index("url")
        property = property.loc[:, ~property.columns.duplicated()].copy()

        self.properties.append(property)
    
    def scrape_all_infos(self):

        #Multithreading for scraping all the tables of all urls
    
        with concurrent.futures.ThreadPoolExecutor() as pool:
            pool.map(self.get_tables, self.list_all_urls)

        #Concatenate all tables for each of the properties into one df

        self.properties = pd.concat(self.properties)

        #Finally saving all properties tables data as a csv 

        self.properties.to_csv("immoweb_properties_data.csv")

scraper = Scraper()
scraper.scrape_all_urls()
scraper.scrape_all_infos()

end = time.perf_counter()
print(round((end - start), 2))