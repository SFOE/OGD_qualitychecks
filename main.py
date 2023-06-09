import pandas as pd
from urllib.request import Request, urlopen, urlretrieve
from bs4 import BeautifulSoup

url = 'https://www.uvek-gis.admin.ch/BFE/ogd/staging/'

def extract_id(fileName):
    ogd_id = fileName.partition('_')[0]
    return ogd_id.replace('ogd', '')
    

def getInformation(url):
    
    #------------------------------------------------------------
    # get file names

    csvList = []

    url = url.replace(" ","%20")
    req = Request(url)
    a = urlopen(req).read()
    soup = BeautifulSoup(a, 'html.parser')
    x = (soup.find_all('a'))
    for i in x:
        file_name = i.extract().get_text()
        if '.csv' in file_name:
            if 'ogd' in file_name:
                csvList.append([file_name, extract_id(file_name)])

    df = pd.DataFrame(csvList, columns= ['fileName', 'ogd_id'])
    df.to_csv('files/info.csv')

getInformation(url)
