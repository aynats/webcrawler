from dataclasses import dataclass
from saver import Saver
from robot_parser import RobotParser
import logging
import re

logging.basicConfig(
    format='%(asctime)s %(bot_id)s%(message)s%(url)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)


@dataclass
class FetchTask:
    tid: int
    maximum_depth: int
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

            logging.info("Веб-краулер обрабатывает", extra={'bot_id': f'[Bot {worker_id}] ', 'url': f': {url}'})
            new_path = self.path + url  # if self.path.endswith('/') else self.path + '/' + url
            name_directory = re.sub(r'\W+', '_', new_path)    # Из ссылки заменяю все, кроме букв, на _
            path, directory = Saver.select_directory(name_directory)
            Saver.save_webpage(url, path, directory)

            try:
                await crawler.crawl(url)
            except Exception as e:
                print(e)
                logging.exception(f'Ошибка обработки: {url}')
            finally:
                crawler.visited_urls.append(url)
                depth += 1
