"""Test suite for logger."""
from collections import Counter
from os import path
from shutil import rmtree
from tempfile import TemporaryDirectory
from unittest.mock import patch
from uuid import uuid4

from log_parser.logger import Logger


def test_logger_connected_hostnames() -> None:
    """Test log connected hostnamees."""
    with TemporaryDirectory() as tmpdir:
        with patch("log_parser.logger.LOGS_DIR", tmpdir):
            logger = Logger()
        logger.log_connected_hostnames('host', {'host-2'})
        expected_lines = [
            "#" * 100 + '\n',
            "The hostnames connected to host are:\n",
            "- host-2\n",
            "#" * 100 + '\n'
        ]
        with open(f"{tmpdir}/info_logs.log") as f:
            assert expected_lines == f.readlines()


def test_logger_resume_last_hour() -> None:
    """Test log resume last hour."""
    with TemporaryDirectory() as tmpdir:
        with patch("log_parser.logger.LOGS_DIR", tmpdir):
            logger = Logger()
        state = {
            'connected_to': {'host-2'},
            'connected_from': {'host-2'},
            'counter_connections': Counter({'host-2': 2, 'origin-host': 1})}
        logger.log_resume_last_hour(1565721477219, 'origin-host', 'end-host', state)
        expected_lines = [
            "#" * 100 + '\n',
            "From 2019-08-13 20:37:57.219000 to 2019-08-13 21:37:57.219000\n",
            "The hostnames connected to end-host are:\n",
            "- host-2\n",
            "-" * 10 + '\n',
            "The hostnames that has been connected from origin-host are:\n",
            "- host-2\n",
            "-" * 10 + '\n',
            "The hostname with more connections is host-2\n",
            "#" * 100 + '\n'
        ]
        with open(f"{tmpdir}/info_logs.log") as f:
            assert expected_lines == f.readlines()
        state = {
            'connected_to': set(),
            'connected_from': set(),
            'counter_connections': Counter()
        }
        logger.log_resume_last_hour(1565721477219, 'origin-host', 'end-host', state)
        expected_lines = [
            "#" * 100 + '\n',
            "From 2019-08-13 20:37:57.219000 to 2019-08-13 21:37:57.219000\n",
            "The hostnames connected to end-host are:\n",
            "- host-2\n",
            "-" * 10 + '\n',
            "The hostnames that has been connected from origin-host are:\n",
            "- host-2\n",
            "-" * 10 + '\n',
            "The hostname with more connections is host-2\n",
            "#" * 100 + '\n',
            "#" * 100 + '\n',
            "From 2019-08-13 20:37:57.219000 to 2019-08-13 21:37:57.219000\n",
            "The hostnames connected to end-host are:\n",
            "-" * 10 + '\n',
            "The hostnames that has been connected from origin-host are:\n",
            "-" * 10 + '\n',
            "There is no connections in the last hour\n",
            "#" * 100 + '\n'
        ]
        with open(f"{tmpdir}/info_logs.log") as f:
            assert expected_lines == f.readlines()


def test_create_dir_if_not_exists() -> None:
    """Check that logger creates dir if not exists."""
    mock_logs_dir = str(uuid4())
    assert not path.isdir(mock_logs_dir)
    with patch("log_parser.logger.LOGS_DIR", mock_logs_dir):
        Logger()
    assert path.isdir(mock_logs_dir)
    rmtree(mock_logs_dir)
