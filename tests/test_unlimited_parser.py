"""Test suite for unlimited parser."""
from collections import Counter
from unittest.mock import call, Mock, patch

from pytest import raises

from log_parser.unlimited_parser import unlimited


class SleepException(Exception):
    """Exception used to stop unlimited parser."""
    pass


@patch('log_parser.unlimited_parser.logger')
@patch('log_parser.unlimited_parser.sleep')
def test_unlimited(mock_sleep: Mock, mock_logger: Mock) -> None:
    """Test unlimited function."""
    def _sleep_side_effect(time: int) -> None:
        raise SleepException
    mock_sleep.side_effect = _sleep_side_effect
    mock_log_resume_last_hour = Mock()
    mock_logger.log_resume_last_hour = mock_log_resume_last_hour
    with raises(SleepException):
        unlimited('tests/data/example.txt', 'Denija', 'Yurith', 1565721477219)

    # assert mock_log_resume_last_hour.call_count == 3
    expected_actual = {
        'connected_to': {'Marybell', 'Nyson', 'Denija', 'Teniyah'},
        'connected_from': {'Vidhu', 'Yurith'},
        'counter_connections': Counter(
            {
                'Yurith': 4, 'Denija': 2, 'Marybell': 1, 'Albany': 1, 'Keden': 1, 'Hasya': 1,
                'Laquarius': 1, 'Nyson': 1, 'Vidhu': 1, 'Teniyah': 1
            }
        )

    }
    calls = [
        call(1565721477219, 'Denija', 'Yurith', expected_actual),
        call(1565725077219, 'Denija', 'Yurith', expected_actual)
    ]
    assert mock_log_resume_last_hour.mock_calls[1] == calls[1]
    mock_log_resume_last_hour.assert_has_calls(calls, any_order=False)
