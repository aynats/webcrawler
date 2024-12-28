import asyncclick as click
import asyncio
import logging
from main import Crawler

logging.basicConfig(
    format='%(asctime)s %(levelname)s: %(message)s',
    level=logging.INFO)


@click.command()
@click.option('--scan', '-s', required=True, type=str, help='URL сканируемого сайта или файл .txt с несколькими URL-ами'
                                                            'Пример: --scan https://example.com или --scan urls.txt')
@click.option('--depth', '-d', default=2, type=int, help='Глубина сканирования ресурса', show_default=True)
@click.option('--path', '-p', default='', help='Директория для скачивания файлов'
                                               'Пример: --path C:/Users/User/directory')
# @click.option('--bots', '-b', default=4, help="Количество ботов для обхода", show_default=True)
async def crawl(site, depth, path, bots):
    async def run_crawler():
        crawler = Crawler(
            site,
            depth=depth,
            directory=path,
            # bots=bots,
        )
        try:
            await crawler.run()
            await asyncio.sleep(.25)
            logging.info("The crawling was ended")
        except Exception as e:
            print(f"An error occurred: {e}")
            await crawler.stop()

    await run_crawler()


if __name__ == '__main__':
    asyncio.run(crawl())
