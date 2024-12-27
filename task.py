from dataclasses import dataclass
from .utils import Utils
from .robot_parser import RobotParser
import logging
import re


logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)


@dataclass
class FetchTask:
    maximum_depth: int
    tid: int
    path: str
    maxsize: int

    async def perform(self, crawler, worker_id, rtypes, ntypes, nurls):
        """
        param: crawler: Краулер
        param: worker_id: Какой бот сейчас обрабатывает запрос
        param: rtypes: Типы файлов, которые хочется скачивать
        param: ntypes: Типы файлов, которые не хочется скачивать
        param: nurls: Ссылки, с которых не хочется ничег скачивать
        """
        depth = 0
        while crawler.urls_to_visit and depth <= self.maximum_depth:

            url = crawler.urls_to_visit.pop(0)
            parser = RobotParser(url)
            parser.parse()
            hot_keys = parser.key_words
            last_folder = re.search(r"/(\S[^/])+$", str(url))

            if not last_folder:
                last_folder = ''
            else:
                last_folder = last_folder.group(0)
            if last_folder in hot_keys["Disallow"] or "/" in hot_keys["Disallow"]:
                return

            logging.info(f' {worker_id} Crawling now: {url}')
            name_folder = self.path + url if self.path.endswith('/') else self.path + '/' + url
            Utils.save_page(url, self.maxsize, rtypes, ntypes, nurls, re.sub(r'\W+', '_', name_folder))

            try:
                await crawler.crawl(url)
            except Exception as e:
                print(e)
                logging.exception(f'Failed to crawl: {url}')
            finally:
                crawler.visited_urls.append(url)
                depth += 1