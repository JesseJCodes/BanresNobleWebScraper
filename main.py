from BookScraper import NYTimesBookScraper
import os
import pandas as pd
from bs4 import BeautifulSoup

#Called NYTimesBookScraper to scrape data then write in to text files as string
#Then I used BS4 to sift through those files for the data
# bs = NYTimesBookScraper()
NY_BEST_FOLDER = os.listdir('NY15ByCategoryScrape')
NY_TIMES_BS_DF = {}
#looping through each file in directory
for f in NY_BEST_FOLDER:
    with open(f'./NY15ByCategoryScrape/{f}', 'r') as file:
        webpage_html = file.read()
        soup = BeautifulSoup(webpage_html, 'html.parser')
        categorys = soup.title.string.split(' ')[6:8]
        #Structure of Data Frame
        NY_TIMES_BS_DF[f"{categorys[0]} {categorys[1]}"] = {
            'Title': [],
            'Author': [],
            'Pub-Date': [],
            'Price': [],
        }


        for s in soup.find_all("div", {"class": "product-info-view"}):
            title = s.findNext("a", {"class": ""}).text
            author = s.findNext("div", {"class": "product-shelf-author"}).text
            pub_date = s.findNext('span', {"class": "publ-date"}).text
            price = s.findNext('a', {"class": "current"}).text
            for l in NY_TIMES_BS_DF:
                NY_TIMES_BS_DF[l]['Title'].append(title)
                NY_TIMES_BS_DF[l]['Author'].append(author)
                NY_TIMES_BS_DF[l]['Pub-Date'].append(pub_date)
                NY_TIMES_BS_DF[l]['Price'].append(price)
#Uploading data to a csv
for dict in NY_TIMES_BS_DF:
    df_title = f"{dict}"
    df = pd.DataFrame(NY_TIMES_BS_DF[dict],columns=['Title', 'Author', 'Pub-Date', 'Price'])
    df.index.name = df_title
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    with open('./top_15NYTimes.csv',"a") as file:
        file.write(f"{title}\n"
                   f"{df}")




