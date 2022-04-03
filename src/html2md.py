from urllib import request
from bs4 import BeautifulSoup as bs

with request.urlopen('https://cloud.google.com/bigquery/docs/introduction?hl=ja') as f:
    soup = bs(f.read())

navi = soup.find('ul', class_='devsite-nav-list', menu='_book')

