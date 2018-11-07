
#importing the required libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv
import numpy as np


#the following method scrapes all the urls from the base url by changing the params and returns a list of urls 
def get_ads_urls():
    urls_list = []
    # define the basic url to crawl on
    basic_url = "https://www.avito.ma/fr/maroc/voitures-à_vendre?mpr=500000000&o="
    # loop over the paginated urls
    for i in range(1,250):
        # get the page url
        url = basic_url+str(i)
        #print(url)
        # get the request response
        r  = requests.get(url)
        data = r.text
        # transform it to bs object
        soup = BeautifulSoup(data, "lxml")
        # loop over page links
        for div in soup.findAll('div', {'class': 'item-img'}):
            a = div.findAll('a')[0]
            urls_list.append(a.get('href'))


    df = pd.DataFrame(data={"url": urls_list})
    df.to_csv("./carsdata/ads_urls.csv", sep=',',index=False)
get_ads_urls()


#THe following method crapes all the data from the given url 

def scrap_ad_data(ad_url):
    r = requests.get(ad_url)
    data = r.text
    soup = BeautifulSoup(data, "html.parser")
    target_component = soup.findAll("h2",  {"class": ["font-normal", "fs12", "no-margin", "ln22"]})
    
    results = []
    for i in target_component:
        results.append(''.join(i.findAll(text=True)).replace('\n',''))
    return results


#

 urls_data = pd.read_csv("./carsdata/ads_urls.csv")

final_result = []
i = 1
for index, row in urls_data.iterrows():
    final_result.append(scrap_ad_data(row['url']))

 with open("./carsdata/output.csv", "w") as f:
 writer = csv.writer(f)
 writer.writerows(final_result)



