"""Connected hostnames.
~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from itertools import zip_longest
import multiprocessing
from typing import Any, Iterable, Iterator, Optional, Union

from log_parser.constants import TIMESTAMP_MARGIN
from log_parser.logger import logger


def grouper(iterable: Union[Iterator, Iterable], n: int, fillvalue: Optional[Any] = None) -> Iterator:
    """Collect data into fixed-length chunks or blocks."""
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def process_batch(batch_lines: Iterable, int_timestamp: int, end_timestamp: int, hostname: str, host_len: int) -> set:
    """Process a batch of lines and returns the set of hostnames that have been conected to hostname."""
    hostnames = set()
    for line in batch_lines:
        if line is None:
            break
        timestamp = int(line[:13])
        if timestamp > end_timestamp + TIMESTAMP_MARGIN:
            break
        if timestamp < int_timestamp:
            continue
        if line[-host_len - 1:-1] != hostname:
            continue
        if timestamp < end_timestamp:
            hostnames.add(line[14:-host_len - 2])
    return hostnames


def _get_connected_hostnames_multithread(input_file: str, int_timestamp: int, end_timestamp: int, hostname: str,
                                         workers: int = 8, batch_size: int = 200000) -> set:
    """Get connected hostnames using multithread."""
    host_len = len(hostname)
    with multiprocessing.Pool(workers) as p:
        batches = iter(
            (batch, int_timestamp, end_timestamp, hostname, host_len) for batch in grouper(open(input_file), batch_size)
        )
        hostnames_list = p.starmap(process_batch, batches)
        return set().union(*hostnames_list)


def _get_connected_hostnames_single_thread(input_file: str, int_timestamp: int, end_timestamp: int,
                                           hostname: str) -> set:
    """Get connected hostnames using single thread."""
    hostnames = set()
    host_len = len(hostname)
    for line in open(input_file):
        timestamp = int(line[:13])
        if timestamp > end_timestamp + TIMESTAMP_MARGIN:
            break
        if timestamp < int_timestamp:
            continue
        if line[-host_len - 1:-1] != hostname:
            continue
        if timestamp < end_timestamp:
            hostnames.add(line[14:-host_len - 2])
    return hostnames


def get_connected_hostnames(input_file: str, int_timestamp: int, end_timestamp: int, hostname: str,
                            use_multithread: bool = False, workers: int = 8, batch_size: int = 200000) -> None:
    """Reads input_file and reports a list hostnames connected to the given host during the given period.

    Args:
        input_file: The file to read.
        int_timestamp: The beginning of the period.
        end_timestamp: The end of the period.
        hostname: The host to check connetions.
        use_multithread: If it's True multithreading is used. { default: False}.
        workers: Number of workers to use if multithreading it's enabled. { default: 8}
        batch_size: Number of lines in each batch (used only in multithreading). { default: 200000}
    """
    workers = workers or 8
    batch_size = batch_size or 200000
    if use_multithread:
        hostnames = _get_connected_hostnames_multithread(
            input_file, int_timestamp, end_timestamp, hostname, workers=workers, batch_size=batch_size)
    else:
        hostnames = _get_connected_hostnames_single_thread(input_file, int_timestamp, end_timestamp, hostname)

    logger.log_connected_hostnames(hostname, hostnames)
