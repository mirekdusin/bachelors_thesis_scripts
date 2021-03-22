import csv
import requests
from concurrent.futures.thread import ThreadPoolExecutor
from bs4 import BeautifulSoup


def get_anchors(div, class_name):
    all_anchors = []
    content = div.find_all('div', class_=class_name)
    
    for cont in content:
        anchors = cont.find_all('a')

        for a in anchors:
            all_anchors.append(a.text.strip())
            
    return sorted(set(all_anchors))


def get_date(div, str_name):
    span = div.select('span.' + str_name)
    return span[0].text.rstrip("\n") if span else ""


def parse_html(i):
    rows = []
    page = requests.get(URL + str(i))
    soup = BeautifulSoup(page.content, 'html.parser')
    content = soup.select('.view-content')
    for cont in content:
        items = cont.select('div.views-row')
        for item in items:
            div = item.select('div.views-field-title')
            if div:
                href = div[0].select('a')
                href = href[0].get('href')
                name = div[0].select('h2')
                capacity = item.select('div.free-spots')
                if capacity:
                    if capacity[0].text.rstrip("\n") == "Kapacita je naplněna.":
                        capacity = 1
                    else:
                        capacity = 0
                else:
                    capacity = 0
                if name:
                    name = name[0].text.rstrip("\n")

                    aim = get_anchors(item, 'views-field-field-aim')
                    activity = get_anchors(item, 'views-field-field-activity')
                    last = get_anchors(item, 'views-field-field-last')
                    age = get_anchors(item, 'views-field-field-age')
                    attendance = get_anchors(item, 'views-field-field-attendance')
                    date_start = get_date(item, 'date-display-start')
                    date_end = get_date(item, 'date-display-end')

                    rows.append(["https://www.dobrovolnik.cz" + href, name, '|'.join(aim), '|'.join(activity),
                           '|'.join(last), '|'.join(age),
                           '|'.join(attendance),date_start, date_end, capacity])
    return rows


executor = ThreadPoolExecutor(8)
futures = []

URL = 'https://www.dobrovolnik.cz/prilezitosti?\
       field_state_value[0]=Archivov%C3%A1no&page='

with open('output.csv', mode='w', newline='') as output:
    output_writer = csv.writer(output,
                               delimiter=',',
                               quotechar='"',
                               quoting=csv.QUOTE_MINIMAL)
                               
    for i in range(176):
        future = executor.submit(parse_html, i)
        futures.append(future)
        
    for future in futures:
        result = future.result()
        for row in result:
            output_writer.writerow(row)
