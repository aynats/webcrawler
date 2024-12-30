from unittest import TestCase
from unittest.mock import patch, MagicMock
from bot_process import BotProcess
import re

class TestBotProcess(TestCase):
    @patch('robot_parser.RobotParser')
    @patch('saver.Saver.save_webpage')
    @patch('crawler.Crawler.crawl')
    def test_process_with_disallowed_url(self, mock_crawl, mock_save_webpage, mock_robot_parser):
        mock_robot = MagicMock()
        mock_robot_parser.return_value = mock_robot
        mock_robot.key_words = {
            'Disallow': ['/disallowed_path']
        }

        crawler = MagicMock()
        crawler.urls_to_visit = ['https://example.com/disallowed_path']
        crawler.visited_urls = []

        bot_process = BotProcess(tid=1, maximum_depth=3, path="test_path")
        bot_process.process(crawler, worker_id=1)
        mock_save_webpage.assert_not_called()

    @patch('robot_parser.RobotParser')
    @patch('saver.Saver.save_webpage')
    @patch('crawler.Crawler.crawl')
    async def test_process_with_allowed_url(self, mock_crawl, mock_save_webpage, mock_robot_parser):
        mock_robot = MagicMock()
        mock_robot_parser.return_value = mock_robot
        mock_robot.key_words = {}

        crawler = MagicMock()
        crawler.urls_to_visit = ['https://example.com/allowed_path']
        crawler.visited_urls = []

        bot_process = BotProcess(tid=1, maximum_depth=3, path="test_path")

        await bot_process.process(crawler, worker_id=1)

        mock_save_webpage.assert_called_once_with(
            'https://example.com/allowed_path',
            'test_pathhttps://example.com/allowed_path',
            'test_pathhttps://example.com/allowed_path_data'
        )

    @patch('robot_parser.RobotParser')
    @patch('saver.Saver.save_webpage')
    @patch('crawler.Crawler.crawl')
    def test_process_with_disallowed_last_folder(self, mock_crawl, mock_save_webpage, mock_robot_parser):
        mock_robot = MagicMock()
        mock_robot_parser.return_value = mock_robot
        mock_robot.key_words = {
            'Disallow': ['/restricted', 'another_folder']
        }

        crawler = MagicMock()
        crawler.urls_to_visit = ['https://example.com/restricted']  # Последний сегмент в Disallow
        crawler.visited_urls = []

        bot_process = BotProcess(tid=1, maximum_depth=1, path="test_path")
        bot_process.process(crawler, worker_id=1)

        mock_save_webpage.assert_not_called()
        mock_crawl.assert_not_called()
