"""Logger class.
~~~~~~~~~~~~~~~~~~
"""
from datetime import datetime
from logging import DEBUG, Formatter, getLogger, INFO, StreamHandler
from logging.handlers import RotatingFileHandler
from os import mkdir, path
from typing import Dict

from log_parser.config import BACKUP_COUNT, LOGS_DIR, MAX_BYTES
from log_parser.constants import HOUR_TIMESTAMP


class Logger():
    """Class used to make easier report the function's output."""
    def __init__(self) -> None:
        """Creates a logger instance.

        This logger uses a RotationFileHandler with a limit of max_bytes.
        """
        if not path.isdir(LOGS_DIR):
            mkdir(LOGS_DIR)
        log_console_format = "%(message)s"
        log_file_format = "[%(levelname)s] - %(asctime)s - %(name)s - : %(message)s in %(pathname)s:%(lineno)d"

        logger = getLogger('log_parser')
        logger.setLevel(INFO)

        console_handler = StreamHandler()
        console_handler.setLevel(INFO)
        console_handler.setFormatter(Formatter(log_console_format))

        file_handler = RotatingFileHandler(f"{LOGS_DIR}/debug_logs.log", maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
        file_handler.setLevel(DEBUG)
        file_handler.setFormatter(Formatter(log_file_format))

        file_handler_info = RotatingFileHandler(f"{LOGS_DIR}/info_logs.log", maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
        file_handler_info.setLevel(INFO)
        file_handler_info.setFormatter(Formatter(log_console_format))

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        logger.addHandler(file_handler_info)
        self.logger = logger

    def info(self, message: str) -> None:
        """Logs info message."""
        self.logger.info(message)

    def log_connected_hostnames(self, end_host: str, hostnames: set) -> None:
        """Logs connected hostnames."""
        self.info("#" * 100)
        self.info(f"The hostnames connected to {end_host} are:")
        for hostname in hostnames:
            self.info(f"- {hostname}")
        self.info("#" * 100)

    def log_resume_last_hour(self, init_timestamp: int, origin_host: str, end_host: str, state: Dict) -> None:
        """Logs the resume of last hour."""
        self.info("#" * 100)
        init_datetime = datetime.fromtimestamp(init_timestamp / 1000)
        end_datetime = datetime.fromtimestamp((init_timestamp + HOUR_TIMESTAMP) / 1000)
        self.info(f"From {init_datetime} to {end_datetime}")
        self.info(f"The hostnames connected to {end_host} are:")
        for hostname in state['connected_to']:
            self.info(f"- {hostname}")
        self.info("-" * 10)
        self.info(f"The hostnames that has been connected from {origin_host} are:")
        for hostname in state['connected_from']:
            self.info(f"- {hostname}")
        self.info("-" * 10)
        max_connections = state['counter_connections'].most_common(1)[0][0] if state['counter_connections'] else None
        if max_connections:
            self.info(f"The hostname with more connections is {max_connections}")
        else:
            self.info("There is no connections in the last hour")
        self.info("#" * 100)


logger = Logger()
