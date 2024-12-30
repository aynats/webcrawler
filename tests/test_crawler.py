import pytest
from unittest.mock import patch
from crawler import Crawler


def test_crawler_initialization_with_valid_file():
    crawler = Crawler(file="sites_crawler.txt", depth=3, directory="test_dir", bots=4)

    assert crawler.file == "sites_crawler.txt"
    assert crawler.depth == 3
    assert crawler.directory == "test_dir"
    assert crawler.bots == 4
    assert crawler.urls_to_visit == ["url1", "url2"]  # Проверить на основе того, что возвращает URLParser
    assert crawler.visited_urls == []


def test_crawler_initialization_with_invalid_file():
    with pytest.raises(ValueError, match="Введите название файла формата .txt или ссылку на ресурс"):
        Crawler(file="invalid_file.doc", depth=3, directory="test_dir", bots=4)


def test_add_url_to_visit():
    crawler = Crawler(file="sites_crawler.txt", depth=3, directory="test_dir", bots=4)
    initial_count = len(crawler.urls_to_visit)  # url1, url2 в sites_crawler.txt
    crawler.add_url_to_visit("https://example.com/new_page")

    # URL должен быть добавлен в список urls_to_visit
    assert len(crawler.urls_to_visit) == initial_count + 1
    assert "https://example.com/new_page" in crawler.urls_to_visit

    # Попытка добавить тот же URL не должна увеличивать длину списка
    crawler.add_url_to_visit("https://example.com/new_page")
    assert len(crawler.urls_to_visit) == initial_count + 1
