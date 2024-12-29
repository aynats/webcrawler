import os
import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class Saver:
    @staticmethod
    def select_directory(page_path: str = ''):
        path, extension = os.path.splitext(page_path)  # Отделяем расширение от имени файла для директории
        directory = path + '_data'
        if not os.path.exists(directory):
            os.mkdir(directory)
        return path, directory

    @staticmethod
    def save_webpage(url: str, path: str, directory: str):
        """
        Сохраняет в директорию страницу
        :param: url: Ссылка на сохраняемую веб-страницу
        :param: page_path: Путь до директории, куда нужно сохранить веб-страницу
        """
        session = requests.Session()
        try:
            response = session.get(url)
        except Exception:
            return

        soup = BeautifulSoup(response.text, "html.parser")
        tags_inner = {
            'img': 'src',
            'link': 'href',
            'script': 'src'
        }
        for tag, attribute in tags_inner.items():   # Поочередно сохраняем медиафайлы нужных типов
            Saver.save_media(soup, directory, session, url, tag, attribute)
            break
        os.chdir(directory)
        with open(path + '.html', 'wb') as file:
            file.write(soup.prettify('utf-8'))
        os.chdir('../')

    @staticmethod
    def save_media(soup: BeautifulSoup, directory: str, session: requests.sessions.Session,
                   url: str, tag: str, attribute: str):
        """
        Сохраняет контент страницы
        :param: soup: BeautifulSoup
        :param: directory: Директория сохранения медиафайлов
        :param: session: Текущая сессия
        :param: tag: img/link/src
        :param: attribute: Аттрибуты в HTML, соответствующие тэгам tag
        """
        for resource in soup.findAll(tag):
            if resource.has_attr(attribute):
                # Разделили название файла и расширение
                filename, extension = os.path.splitext(os.path.basename(resource[attribute]))
                filename = re.sub(r'\W+', '', filename) + extension    # Взяли только буквенные символы в названии
                file_url = urljoin(url, resource.get(attribute))    # Оффлайн-доступ к медиафайлам. Заменяем ссылки
                filepath = os.path.join(directory, filename)
                resource[attribute] = os.path.join(os.path.basename(directory), filename)

                try:
                    if not os.path.isfile(filepath):
                        with open(filepath, 'wb') as file:
                            file_bin = session.get(file_url)
                            file.write(file_bin.content)
                except Exception:
                    pass
