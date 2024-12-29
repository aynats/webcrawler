from saver import Saver
import re
import pytest
import os
from pathlib import Path


def test_select_directory(tmp_path):
    test_page_path = tmp_path / 'test_directory'
    name_directory = str(test_page_path)
    expected_directory = name_directory + '_data'

    path, final_directory = Saver.select_directory(name_directory)

    assert path == name_directory
    assert final_directory == expected_directory

    assert os.path.exists(final_directory)
    assert os.path.isdir(final_directory)
