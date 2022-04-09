import sys
from urllib import request
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup as bs


target_url = sys.argv[1] 

parse_results = urlparse(target_url)
base = f'{parse_results.scheme}://{parse_results.netloc}'
export_filename = f'{parse_results.path.split("/")[1]}.md'

with request.urlopen(target_url) as f:
    soup = bs(f.read(), 'html.parser')

contents = []
navi = soup.find('ul', class_='devsite-nav-list', menu='_book')
for li in navi.findAll('li', recursive=False):
    li_class = li['class']
    if 'devsite-nav-preview' in li_class:
        continue
    if 'devsite-nav-heading' in li_class:
        contents.append(f'## {li.text.strip()}')
    for a in li.findAll('a', class_='devsite-nav-title'):
        contents.append(f'### [{a.text.replace(" ", "")}]({urljoin(base, a.get("href"))})')

with open(export_filename, 'w', encoding='utf-8') as f:
    f.writelines('\n'.join(contents))