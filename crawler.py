import asyncio
import logging
from task import FetchTask
from typing import Optional
from URL_parser import URLParser
from domains_parser import DomainParser

logging.basicConfig(
    format='%(asctime)s %(bot_id)s%(message)s%(url)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)


class Crawler:
    def __init__(self, file, depth: int = 2, directory: str = '', bots: int = 4, domain: str = ''):
        if file.endswith('.txt') or file.startswith("http"):
            self.file = file
        else:
            raise ValueError("Введите название файла формата .txt или ссылку на ресурс")
        self.urls_to_visit = URLParser.get_urls_from_txt(self.file) if self.file.endswith('txt') else [self.file]
        self.visited_urls = []
        self.max_rate = 3
        self.interval = 5
        self.is_crawled = False
        self.tasks_queue = asyncio.Queue()
        self._scheduler_task: Optional[asyncio.Task] = None
        self.concurrent_workers = 0
        self.stop_event = asyncio.Event()
        self.bots = bots
        self.depth = depth
        self.directory = directory
        self.domain = DomainParser.get_domains_from_txt(domain) if domain and domain.endswith(".txt") else [domain]

    async def _worker(self, task, tid):
        async with asyncio.Semaphore(self.max_rate):
            self.concurrent_workers += 1
            await task.perform(self, tid)
            self.tasks_queue.task_done()
        self.concurrent_workers -= 1
        if not self.is_crawled and self.concurrent_workers == 0:
            self.stop_event.set()

    async def stop(self):
        self.is_crawled = False
        self._scheduler_task.cancel()
        if self.concurrent_workers != 0:
            await self.stop_event.wait()

    async def _scheduler(self):
        a = []
        while self.is_crawled:
            for _ in range(self.max_rate):
                task = await self.tasks_queue.get()
                a.append(asyncio.create_task(self._worker(task, task.tid)))
            await asyncio.sleep(self.interval)

    def add_url_to_visit(self, url):
        if url not in self.visited_urls and url not in self.urls_to_visit:
            self.urls_to_visit.append(url)

    async def crawl(self, url):
        html = await URLParser.get_webpage_html(url)
        if html is not None:
            for current_url in URLParser.take_linked_urls(url, html):
                if self.domain == [''] or DomainParser.is_allowed_domain(current_url, self.domain):
                    if (current_url and current_url.find('captcha') == -1
                            and not current_url.endswith("rst")
                            and not current_url.startswith("../")):
                        self.add_url_to_visit(current_url)

    async def run(self):
        for i in range(1, self.bots):
            await self.tasks_queue.put(FetchTask(tid=i,
                                                 maximum_depth=self.depth,
                                                 path=self.directory))
        self.is_crawled = True
        self._scheduler_task = asyncio.create_task(self._scheduler())
        await self.tasks_queue.join()
        await self.stop()
