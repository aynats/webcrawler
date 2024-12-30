from unittest.mock import mock_open
import unittest
import pytest
import os
from unittest.mock import patch, MagicMock
from saver import Saver
import requests
from bs4 import BeautifulSoup
import re


def test_select_directory(tmp_path):
    test_page_path = tmp_path / 'test_directory'
    name_directory = str(test_page_path)
    expected_directory = name_directory + '_data'

    path, final_directory = Saver.select_directory(name_directory)

    assert path == name_directory
    assert final_directory == expected_directory

    assert os.path.exists(final_directory)
    assert os.path.isdir(final_directory)


@pytest.mark.parametrize("url", ["https://example.com"])
@patch("requests.Session.get")
def test_save_webpage_success(mock_get, url, tmp_path):
    mock_response = MagicMock()
    mock_response.text = "<html><body><h1>Test</h1></body></html>"
    mock_get.return_value = mock_response

    test_page_path = tmp_path / re.sub(r'\W+', '_', url)
    name_directory = str(test_page_path)
    path, directory = Saver.select_directory(name_directory)    # path - имя дир-ии от ссылки, директория - полное имя

    with patch.object(Saver, 'save_media'):
        Saver.save_webpage(url, path, directory)
        assert os.path.exists(directory), f"Директория {directory} не была создана"
        os.chdir(directory)

        html_file = f"{path}.html"
        assert os.path.exists(html_file), f"Файл {html_file} не был создан"


@pytest.mark.parametrize("url, path, directory", [
    ("https://example.com", "/some/path/to/file", "some/directory")
])
@patch("requests.Session.get")
def test_save_webpage_exception_handling(mock_get, url, path, directory):
    mock_get.side_effect = requests.exceptions.RequestException("Request failed")
    with patch("os.path.exists", return_value=False), patch("os.mkdir"):
        result = Saver.save_webpage(url, path, directory)
        assert result is None, "При возникновении исключения результат должен быть None"


class TestSaver(unittest.TestCase):
    @patch('saver.requests.Session')
    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open)
    def test_save_media_new_file(self, mock_open_func, mock_isfile, mock_requests):
        mock_isfile.return_value = False  # Файл не существует
        mock_session = MagicMock()
        mock_requests.return_value = mock_session

        html_content = '''
        <html>
            <body>
                <img src="https://example.com/image1.jpg">
                <link href="https://example.com/style.css">
                <script src="https://example.com/script.js"></script>
            </body>
        </html>
        '''
        soup = BeautifulSoup(html_content, 'html.parser')
        directory = 'test_data'

        # Вызов метода
        Saver.save_media(soup, directory, mock_session, 'https://example.com', 'img', 'src')

        # Проверяем, что файл был открыт для записи
        mock_open_func.assert_called_with(os.path.join(directory, 'image1.jpg'), 'wb')

        # Проверяем, что был выполнен запрос на загрузку изображения
        mock_session.get.assert_called_with('https://example.com/image1.jpg')

    @patch('saver.requests.Session')
    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open)
    def test_save_media_existing_file(self, mock_open_func, mock_isfile, mock_requests):
        # Настройка
        mock_isfile.return_value = True  # Файл существует
        mock_session = MagicMock()
        mock_requests.return_value = mock_session

        html_content = '''
            <html>
                <body>
                    <img src="https://example.com/image1.jpg">
                </body>
            </html>
            '''
        soup = BeautifulSoup(html_content, 'html.parser')
        directory = 'test_data'

        # Вызов метода
        Saver.save_media(soup, directory, mock_session, 'https://example.com', 'img', 'src')

        # Проверяем, что файл не был открыт для записи, так как он уже существует
        mock_open_func.assert_not_called()

        # Проверяем, что запрос на загрузку изображения не был выполнен
        mock_session.get.assert_not_called()
