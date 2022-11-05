import sys
from urllib import request
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup as bs


def extract(soup, pr):
    contents = []
    base = f'{pr.scheme}://{pr.netloc}'

    navi = soup.find('ul', class_='devsite-nav-list', menu='_book')
    for li in navi.findAll('li', recursive=False):
        li_class = li['class']
        if 'devsite-nav-preview' in li_class:
            continue
        if 'devsite-nav-heading' in li_class:
            contents.append(f'## {li.text.strip()}')
        for a in li.findAll('a', class_='devsite-nav-title'):
            contents.append(f'### [{a.text.replace(" ", "")}]({urljoin(base, a.get("href"))})')

    return contents
    
def get_soup(url):
    with request.urlopen(url) as f:
        soup = bs(f.read(), 'html.parser')

    return soup
    
def export(contents, pr):
    pathes = pr.path.split("/")
    service_name = pathes[1]
    if service_name == 'ai-platform':
        service_name = f'{service_name}-{pathes[2]}'
    elif service_name == 'memorystore':
        service_name = f'{service_name}-{pathes[3]}'
        
    with open(f'{service_name}.md', 'w', encoding='utf-8') as f:
        f.writelines('\n'.join(contents))


if __name__ == '__main__':
    with open(sys.argv[1], encoding='utf-8') as f:
        urls = f.readlines()
        
    for url in urls:
        pr = urlparse(url)
        soup = get_soup(url)
        contents = extract(soup, pr)
        export(contents, pr)
