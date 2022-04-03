from urllib import request
from bs4 import BeautifulSoup as bs

res = request.urlopen('https://cloud.google.com/bigquery/docs/introduction?hl=ja')
soup = bs(res)
res.close()
navi = soup.find('ul', class_='devsite-nav-list', menu='_book')

