import re
import asyncio
import json
import os

import aiohttp
from aiofile import async_open
from aiohttp_retry import RetryClient, ExponentialRetry
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

from get_all_links import get_all_links


headers = {
    'user-agent': UserAgent().random
}

async def parse_direction_page(session: aiohttp.ClientSession, url: str):
    DATA = {}

    retry_settings = ExponentialRetry(attempts=5)
    retry_client = RetryClient(session)
    async with retry_client.get(url) as resp:
        if resp.ok:
            soup = BeautifulSoup(await resp.text(), 'lxml')
            p = soup.find('p').text
            for line in map(lambda x: x.strip(), p.split('\n')):
                if 'Направление' in line:
                    code = line.split(': ')[-1].split()[0]
                if 'Образовательная программа' in line:
                    title = ' '.join(line.split(': ')[-1].split()[1:])
                elif 'КЦП по конкурсу: ' in line:
                    DATA['Бюджетных мест'] = int(line.split(': ')[-1])
            DATA["Направление"] = code + ' ' + title

            DATA['Конкурс'] = {}
            for tr in map(lambda x: x.find_all('td'), soup.find('tbody').find_all('tr')):
                pos = int(tr[0].text)
                snils = tr[1].text  # или уникальный код поступающего!
                bvi = tr[2].text == 'Без ВИ'
                priority = int(tr[3].text)
                try:
                    ball = int(tr[4].text.split(',')[0] if not bvi else tr[9].text)
                except ValueError:
                    ball = 0
                DATA['Конкурс'][snils] = {
                     'Приоритет': priority,
                     'Место в списке': pos,
                     'Без ВИ': bvi,
                     'Баллы': ball
                }
            async with async_open(f'parsed_data/{DATA["Направление"]}.json', 'w') as f:
                s = json.dumps(DATA, ensure_ascii=False, indent=4)
                await f.write(s)


async def update_lists():
    if not os.path.isfile('links.txt'):
        get_all_links()

    if not os.path.isdir('parsed_data'):
        os.mkdir('parsed_data')

    async with aiohttp.ClientSession(headers=headers) as session:
        with open('links.txt', 'r') as f:
            for line in f:
                link =line.strip()
                await parse_direction_page(session, link)


if __name__ == '__main__':
    asyncio.run(updaupdate_listste())