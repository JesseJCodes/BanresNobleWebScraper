from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time


headers = {
    "Accept-Language": "en-US,en;q=0.9,pt;q=0.8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
}
BN_BEST_SELLERS = "https://www.barnesandnoble.com/b/the-new-york-times-bestsellers/_/N-1p3n"
BN_BEST_SELLERS_CATERGORYS = ""

"""This Class below Scrapes NYTimes Best Sellers off of the Barnes and Noble Website"""
"""I had issues with hang up on line 31  with bs request so I just made it write to a directory with each file on the html data as a string scrapped,
then in turn used those files to use bs4 to sift through data and compile a pandas df/csv"""
class NYTimesBookScraper:
    def __init__(self):
        self.response = requests.get(BN_BEST_SELLERS,headers=headers)
        self.webpage = self.response.text
        self.bs = BeautifulSoup(self.webpage, "html.parser")
        self.categorys = self.bs.find_all("li")
        self.category_list = [{c.text:[]} for c in self.categorys]
        self.category_list = [{key.replace('\n','') for key in dicti} for dicti in self.category_list]
        self.category_list = self.category_list[:27]
        top_15_by_cat_ny = [link.get('href') for link in self.bs.find_all("a",class_="see-all-link")]
        for href in top_15_by_cat_ny:
            response = requests.get(f"https://www.barnesandnoble.com{href}", headers=headers)
            self.pages = response.text
            self.soup = BeautifulSoup(response.text, "html.parser")
            string = str(self.soup)
            with open(f"NY15ByCategoryScrape/{self.soup.title.text}"+".html","w") as file:
                file.write(string)