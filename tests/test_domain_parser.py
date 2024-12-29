import pytest
from domains_parser import DomainParser


def test_is_allowed_domain():
    allowed_url = 'http://example.com'
    unresolved_url = 'http://test.org'
    allowed_domains = ['example.com']
    assert DomainParser.is_allowed_domain(allowed_url, allowed_domains), f'{allowed_url} должен быть включен в список доменов {allowed_domains}'
    assert not DomainParser.is_allowed_domain(unresolved_url, allowed_domains), f'{unresolved_url} не должен быть включен в список доменов {allowed_domains}'


def test_is_allowed_domain_if_empty():
    allowed_url = 'http://example.com'
    allowed_domains = ['']
    assert DomainParser.is_allowed_domain(allowed_url, allowed_domains), f'{allowed_url} должен быть включен в список доменов {allowed_domains}'


def test_get_domains_from_txt(tmp_path):
    """Тест чтения доменов из файла."""
    file_content = "example.com\ntest.org\ntwice.extra.ru"
    file = tmp_path / "domains.txt"
    file.write_text(file_content)

    domains = DomainParser.get_domains_from_txt(str(file))
    expected_domains = ["example.com", "test.org", "twice.extra.ru"]
    assert domains == expected_domains, f"Ожидались ссылки {expected_domains}, но получили {domains}"


def test_get_urls_from_txt_empty_file(tmp_path):
    """Тест обработки пустого файла."""
    file = tmp_path / "empty.txt"
    file.write_text("")

    domains = DomainParser.get_domains_from_txt(str(file))
    assert domains == [''], "Для пустого файла должен возвращаться пустой список"
