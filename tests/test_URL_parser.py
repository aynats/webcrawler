import pytest
from unittest.mock import MagicMock
from URL_parser import URLParser


@pytest.mark.asyncio
async def test_get_webpage_html_success():
    """Тест успешного получения HTML-страницы."""
    url = "https://example.com"
    html = await URLParser.get_webpage_html(url)
    assert html is not None, "HTML должен быть загружен"
    assert "<html" in html and "</html>" in html, "Должен содержать HTML-теги"


@pytest.mark.asyncio
async def test_get_webpage_html_invalid_url():
    """Тест обработки несуществующего URL."""
    url = "http://invalid-url.test"
    html = await URLParser.get_webpage_html(url)
    assert html is None, "Для недоступного URL функция должна вернуть None"


def test_take_linked_urls_simple_html():
    """Тест извлечения ссылок из HTML."""
    html = """
    <html>
        <body>
            <a href="https://example.com/page1">Page 1</a>
            <a href="/page2">Page 2</a>
            <a href="#fragment">Fragment</a>
            <a href="mailto:test@example.com">Email</a>
        </body>
    </html>
    """
    url = "https://example.com"
    expected_links = [
        "https://example.com/page1",
        "https://example.com/page2"
    ]
    extracted_links = list(URLParser.take_linked_urls(url, html))
    assert extracted_links == expected_links, f"Ожидались ссылки {expected_links}, но получили {extracted_links}"


def test_get_urls_from_txt(tmp_path):
    """Тест чтения ссылок из файла."""
    file_content = "https://example.com\nhttps://test.com"
    file = tmp_path / "urls.txt"
    file.write_text(file_content)

    urls = URLParser.get_urls_from_txt(str(file))
    expected_urls = ["https://example.com", "https://test.com"]
    assert urls == expected_urls, f"Ожидались ссылки {expected_urls}, но получили {urls}"


def test_get_urls_from_txt_empty_file(tmp_path):
    """Тест обработки пустого файла."""
    file = tmp_path / "empty.txt"
    file.write_text("")

    urls = URLParser.get_urls_from_txt(str(file))
    assert urls == [''], "Для пустого файла должен возвращаться пустой список"


@pytest.mark.asyncio
async def test_get_webpage_html_exception_handling():
    """Тест обработки общего исключения."""
    url = "https://example.com"
    with pytest.raises(Exception):
        async def mock_get():
            raise Exception("Mocked exception")

        URLParser.get_webpage_html = MagicMock(side_effect=mock_get)

        result = await URLParser.get_webpage_html(url)
        assert result is None, "При возникновении исключения функция должна вернуть None"
