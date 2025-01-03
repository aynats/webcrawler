import asyncclick as click
import asyncio
import logging
from crawler import Crawler

logging.basicConfig(
    format='%(asctime)s %(bot_id)s%(message)s%(url)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)


@click.command()
@click.option('--scan', '-s', required=True, type=str, help='URL сканируемого сайта или файл .txt с несколькими URL-ами\n'
                                                            'Пример: --scan https://example.com или --scan urls.txt')
@click.option('--depth', '-d', default=3, type=int, help='Глубина сканирования ресурса', show_default=True)
@click.option('--path', '-p', default='', help='Директория для скачивания файлов\n'
                                               'Пример: --path C:/Users/User/directory')
@click.option('--bots', '-b', default=4, help="Количество ботов для обхода", show_default=True)
@click.option('--domain', '-dm', default='', type=str, help="Переход только по ссылкам указанного домена\n"
                                                            'Пример: --domain example.org или --domain domains.txt')
async def crawl(scan: str, depth: int, path: str, bots: int, domain: str):
    async def run_crawler():
        crawler = Crawler(
            scan,
            depth=depth,
            directory=path,
            bots=bots,
            domain=domain
        )
        try:
            await crawler.run()
            await asyncio.sleep(.25)
            logging.info("Загрузка содержимого страниц закончена.", extra={'bot_id': '', 'url': ''})
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            await crawler.stop()

    await run_crawler()


if __name__ == '__main__':
    asyncio.run(crawl())
