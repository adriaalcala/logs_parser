"""Unlimited parser.
~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from collections import Counter
from copy import deepcopy
from datetime import datetime
from time import sleep

from log_parser.constants import HOUR_TIMESTAMP, TIMESTAMP_MARGIN
from log_parser.logger import logger


def unlimited(log_file: str, origin_host: str, end_host: str, init_timestamp: int = 0) -> None:
    """Parse log_file and once per hour resume logs.

    The resume contains:
       - a list of hostnames connected to a given host during
       - a list of hostnames received connections from a given host
       - the hostname that generated most connections

    Args:
        log_file: The file to parse
        origin_host: The hostname to report the list of hostnames connected to
        end_host: The hostname to report the list of hostnames connected from
        init_timestamp: The timestamp to start report
    """
    init_timestamp = init_timestamp or int(datetime.now().timestamp() * 1000)
    default: dict = {'connected_to': set(), 'connected_from': set(), 'counter_connections': Counter()}
    actual = deepcopy(default)
    next_hour = deepcopy(default)
    with open(log_file, 'r') as f:
        while True:
            line = f.readline()
            if line:
                timestamp_str, origin, end = line.split()
                timestamp = int(timestamp_str)
                if timestamp < init_timestamp:
                    continue
                if timestamp >= init_timestamp + HOUR_TIMESTAMP + TIMESTAMP_MARGIN:
                    logger.log_resume_last_hour(init_timestamp, origin_host, end_host, actual)
                    actual = deepcopy(next_hour)
                    next_hour = deepcopy(default)
                    init_timestamp += HOUR_TIMESTAMP
                if timestamp >= init_timestamp + HOUR_TIMESTAMP:
                    if origin == origin_host:
                        next_hour['connected_from'].add(end)
                    if end == end_host:
                        next_hour['connected_to'].add(origin)
                    next_hour['counter_connections'][origin] += 1
                    next_hour['counter_connections'][end] += 1
                    continue
                if origin == origin_host:
                    actual['connected_from'].add(end)
                if end == end_host:
                    actual['connected_to'].add(origin)
                actual['counter_connections'][origin] += 1
                actual['counter_connections'][end] += 1
            else:
                if datetime.now().timestamp() >= (init_timestamp + HOUR_TIMESTAMP + TIMESTAMP_MARGIN) / 1000:
                    logger.log_resume_last_hour(init_timestamp, origin_host, end_host, actual)
                    init_timestamp += HOUR_TIMESTAMP
                    actual = deepcopy(next_hour)
                    next_hour = deepcopy(default)
                sleep(10.1)
