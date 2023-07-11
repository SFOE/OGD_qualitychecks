import pandas as pd
from urllib.request import Request, urlopen, urlretrieve
from bs4 import BeautifulSoup
import re

url = 'https://www.uvek-gis.admin.ch/BFE/ogd/staging/'

def extract_id(fileName):
    ogd_id = fileName.partition('_')[0]
    return ogd_id.replace('ogd', '')
    

def getInformation(url):
  
  csvList = []
  url = url.replace(" ","%20")
  req = Request(url)
  a = urlopen(req).read()
  soup = BeautifulSoup(a, 'html.parser')
  x = (soup.find_all('a'))
  
  for elem in x:
    stringElem = str(elem)

    if 'csv' in stringElem:
      fileName = re.search('href="(.*)"', stringElem).group(1)
      csvList.append([fileName, extract_id(fileName)])

  df = pd.DataFrame(csvList, columns= ['fileName', 'ogd_id'])
  df.to_csv('files/info.csv')

getInformation(url)
