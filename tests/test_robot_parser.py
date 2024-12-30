import pytest
from unittest.mock import patch, Mock
from robot_parser import RobotParser
import requests


def test_robot_parser_initialization_valid_url():
    """Тест: корректная инициализация с валидным URL."""
    parser = RobotParser("https://example.com/")
    assert parser.url.group(0) == "https://example.com"
    assert parser.robots_txt_path == "https://example.com/robots.txt"

    parser = RobotParser("https://example.com")
    assert parser.url.group(0) == "https://example.com"
    assert parser.robots_txt_path == "https://example.com/robots.txt"


def test_robot_parser_initialization_invalid_url():
    """Тест: инициализация с некорректным URL."""
    parser = RobotParser("invalid-url")
    assert parser.url is None
    assert parser.robots_txt_path == ""


@patch("robot_parser.requests.get")
def test_parse_valid_robots_txt(mock_get):
    """Тест: парсинг валидного robots.txt."""
    mock_response = Mock()
    mock_response.text = """User-agent: *\nDisallow: /private/\nAllow: /public/\nCrawl-delay: 10\nRequest-rate: 1/5\nVisit-time: 0600-0845\n"""
    mock_get.return_value = mock_response

    parser = RobotParser("https://example.com/")
    parser.parse()

    assert "*" in parser.key_words["User-agent"]
    assert "/private/" in parser.key_words["Disallow"]
    assert "/public/" in parser.key_words["Allow"]
    assert "10" in parser.key_words["Crawl-delay"]
    assert "1/5" in parser.key_words["Request-rate"]
    assert "0600-0845" in parser.key_words["Visit-time"]


@patch("robot_parser.requests.get")
def test_parse_non_wide_user_agent(mock_get):
    """Тест: парсинг валидного robots.txt."""
    mock_response = Mock()
    mock_response.text = """User-agent: yandexbot\n"""
    mock_get.return_value = mock_response

    parser = RobotParser("https://example.com/")
    parser.parse()

    assert len(parser.key_words["User-agent"]) == 0


@patch("robot_parser.requests.get")
def test_parse_twice_user_agent(mock_get):
    """Тест: парсинг валидного robots.txt."""
    mock_response = Mock()
    mock_response.text = """User-agent: *\nUser-agent: *\n"""
    mock_get.return_value = mock_response

    parser = RobotParser("https://example.com/")
    parser.parse()

    assert len(parser.key_words["User-agent"]) == 1


@patch("robot_parser.requests.get")
def test_parse_no_robots_txt(mock_get):
    """Тест: обработка недоступного robots.txt."""
    mock_get.side_effect = requests.exceptions.RequestException

    parser = RobotParser("https://example.com/")
    parser.parse()

    assert len(parser.key_words["User-agent"]) == 0
    assert len(parser.key_words["Disallow"]) == 0


def test_parse_no_url():
    """Тест: парсинг без URL."""
    parser = RobotParser()
    parser.parse()
    assert len(parser.key_words["User-agent"]) == 0
    assert len(parser.key_words["Disallow"]) == 0


def test_key_words_structure():
    """Тест: структура key_words после инициализации."""
    parser = RobotParser("https://example.com/")
    assert isinstance(parser.key_words, dict)
    for key in ["User-agent", "Disallow", "Allow", "Crawl-delay", "Request-rate", "Visit-time"]:
        assert key in parser.key_words
        assert isinstance(parser.key_words[key], set)
