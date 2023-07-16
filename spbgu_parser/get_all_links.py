import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


def get_all_links():
    domain = 'https://cabinet.spbu.ru/Lists/1k_EntryLists/'
    headers = {
        'user-agent': UserAgent().random
    }
    resp = requests.get(domain+'index_comp_groups.html', headers=headers)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'lxml')

    links = []
    for a in soup.find_all('a'):
        if a.text == 'Госбюджетная':
            links.append(domain+a['href'])

    with open('links.txt', 'w') as f:
        f.write('\n'.join(links))