import re
from urllib.parse import urlparse


class DomainParser:
    @staticmethod
    def get_domains_from_txt(file: str):
        """
        Получает список доменов из файла .txt
        :param file: Файл .txt со списком разрешенных доменов
        :return: Список доменов из файла .txt
        """
        with open(file) as f:
            domains = re.split(r'\n', f.read())
        return domains

    @staticmethod
    def is_allowed_domain(url: str, allowed_domains: list) -> bool:
        """
        Проверяет, принадлежит ли домен ссылки списку разрешённых доменов.
        :param url: Ссылка, которую нужно проверить
        :param allowed_domains: Список разрешённых доменов (пустой = разрешить все)
        :return: True, если домен разрешён, иначе False
        """
        if allowed_domains == ['']:  # Если список пуст, разрешить все
            return True
        parsed_domain = urlparse(url).netloc
        return any(parsed_domain.endswith(domain) for domain in allowed_domains)
