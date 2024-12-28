import aiohttp
import os
import re
import requests

from urllib.request import urlopen
from urllib.parse import urljoin
from bs4 import BeautifulSoup


class Parser:
    @staticmethod
    async def get_webpage_html(url: str):
        """
        Получает содержимое запрошенной веб-страницы
        :param url: Ссылка на страницу
        :return: Содержимое страницы
        """
        try:
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(url) as response:
                        return await response.text()
                except Exception:
                    return
        except ConnectionRefusedError:
            pass

    @staticmethod
    def take_linked_urls(url: str, html: str):
        """
        Извлекает все гиперссылки из текущей веб-страницы
        :param url: Ссылка на текущую веб-страницу
        :param html: HTML-содержимое текущей веб-страницы
        :return: Ссылки, находящаяся на текущей веб-странице
        """
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):     # гиперссылка: HTML-тег <a>
            path = link.get('href')     # непосредственно ссылка
            if path and path.startswith('/'):
                path = urljoin(url, path)
            if path and path.startswith('mail'):    # пропуск "mailto:" и т.п.
                continue
            yield path
