from csv import reader
import requests
from concurrent.futures.thread import ThreadPoolExecutor
from bs4 import BeautifulSoup

def parse_html(url):
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')
    content = soup.select('div.published')
    return content[0].text.rstrip("\n")


executor = ThreadPoolExecutor(8)
futures = []

with open('urls.csv', 'r') as read_obj:
    csv_reader = reader(read_obj, delimiter=',', quotechar='"')
    for row in csv_reader:
        if row[0]:
            future = executor.submit(parse_html, row[0])
            futures.append(future)

    for future in futures:
        print(future.result())
