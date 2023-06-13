import pandas as pd
import re
from urllib.request import Request, urlopen, urlretrieve
from bs4 import BeautifulSoup

url = 'https://www.uvek-gis.admin.ch/BFE/ogd/staging/'

def read_url(url):
  
  csvList = []
  url = url.replace(" ","%20")
  req = Request(url)
  a = urlopen(req).read()
  soup = BeautifulSoup(a, 'html.parser')
  x = (soup.find_all('a'))
  
  for elem in x:
    stringElem = str(elem)

    if 'csv' in stringElem:
      csvList.append(re.search('href="(.*)"', stringElem).group(1))

  df = pd.DataFrame(csvList, columns= ['fileNames'])
  df.to_csv('files/fileNames.csv')

read_url(url)
