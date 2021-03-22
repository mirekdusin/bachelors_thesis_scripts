import csv
import requests
from concurrent.futures.thread import ThreadPoolExecutor
from bs4 import BeautifulSoup

soup = BeautifulSoup(open("./hearth.html"), "html.parser")
content = soup.select('.item-common')
for cont in content:
    type_ = ""
    keywords = list()

    name = cont.find('span', attrs={'test-beacon': 'marketplace-item-post-title'})
    name = name.text.strip()

    offer = cont.find('span', attrs={'class': 'color-offer'})
    if offer:
        type_ = offer.text.strip()

    primary = cont.find('span', attrs={'class': 'color-primary'})
    if primary:
        type_ = primary.text.strip()

    need = cont.find('span', attrs={'class': 'color-need'})
    if need:
        type_ = need.text.strip()

    li = cont.find_all('li', attrs={'test-beacon': 'marketplace-keywords'})
    if li:
        for l in li:
            keywords.append(l.text.strip())

    print(name + "," + type_ + "," + '|'.join(keywords))
