from dataclasses import dataclass
from saver import Saver
from robot_parser import RobotParser
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

    async def perform(self, crawler, worker_id: int):
        """
        Обходит адреса в пределах глубины сканирования
        param: crawler: Crawler
        param: worker_id: Порядковый номер бота, обрабатывающего запрос
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
            new_path = self.path + url  # if self.path.endswith('/') else self.path + '/' + url
            name_directory = re.sub(r'\W+', '_', new_path)    # Из ссылки заменяю все, кроме букв, на _
            path, directory = Saver.select_directory(name_directory)
            Saver.save_webpage(url, path, directory)

            try:
                await crawler.crawl(url)
            except Exception as e:
                print(e)
                logging.exception(f'Failed to crawl: {url}')
            finally:
                crawler.visited_urls.append(url)
                depth += 1
