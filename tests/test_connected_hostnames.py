"""Test suite for connected hostnames."""
from typing import Iterable, List
from unittest.mock import Mock, patch

from pytest import mark, raises

from log_parser.connected_hostnames import get_connected_hostnames, grouper, process_batch


@mark.parametrize("iterable,n,expected", [
    [range(5), 2, [(0, 1), (2, 3), (4, None)]],
    [range(5), 6, [(0, 1, 2, 3, 4, None)]],
    [list(range(5)), 2, [(0, 1), (2, 3), (4, None)]],
    [list(range(5)), 6, [(0, 1, 2, 3, 4, None)]]
])
def test_grouper(iterable: Iterable, n: int, expected: List) -> None:
    """Test grouper."""
    assert list(grouper(iterable, n)) == expected


def test_process_batch_end_time() -> None:
    """Check process batch."""
    batch_lines = iter([
        '1000000000000 host-A host-H\n',
        '1000000000001 host-B host-H\n',
        '1000000000002 host-A host-H2\n',
        '1000000000005 host-D host-H\n',
        '1000000000002 host-C host-H\n',
        '1000000300007 host-E host-H\n',
        '1000000300005 host-E host-H\n',
    ])
    expected_hostnames = set(['host-B', 'host-C'])
    assert process_batch(batch_lines, 1000000000001, 1000000000003, 'host-H', 6) == expected_hostnames
    assert next(batch_lines) == '1000000300005 host-E host-H\n'


def test_process_batch_end_batch() -> None:
    """Check process batch."""
    batch_lines = iter([
        '1000000000000 host-A host-H\n',
        '1000000000001 host-B host-H\n',
        '1000000000002 host-A host-H2\n',
        '1000000000005 host-D host-H\n',
        '1000000000002 host-C host-H\n',
        '1000000000007 host-E host-H\n',
        None
    ])
    expected_hostnames = set(['host-B', 'host-C'])
    assert process_batch(batch_lines, 1000000000001, 1000000000003, 'host-H', 6) == expected_hostnames
    with raises(StopIteration):
        next(batch_lines)


@mark.parametrize("multithread", [False, True])
@patch("log_parser.connected_hostnames.logger")
def test_get_connected(mock_logger: Mock, multithread: bool) -> None:
    """Check get connected."""
    mock_log_connected = Mock()
    mock_logger.log_connected_hostnames = mock_log_connected
    expected = set(['Nyson', 'Denija'])
    get_connected_hostnames(
        'tests/data/example.txt', 1565721488843, 1565721500212, 'Yurith', use_multithread=multithread)
    mock_log_connected.assert_called_once_with('Yurith', expected)
