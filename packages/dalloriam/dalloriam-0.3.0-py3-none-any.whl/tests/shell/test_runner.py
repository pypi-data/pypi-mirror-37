from dalloriam.shell import runner

from typing import List

from unittest import mock

import pytest


@pytest.mark.parametrize(
    'silent,arguments,want_stdout,status,want_err',
    [
        (True, ['docker', 'run', 'stuff'], True, 0, False),
        (False, ['docker', 'run', 'stuff'], False, 0, False),
        (False, ['docker', 'run', 'stuff'], False, 1, True),
    ]
)
def test_run(silent: bool, arguments: List[str], want_stdout: bool, status: int, want_err: bool):
    try:
        with mock.patch.object(runner, 'call', return_value=status) as mock_call:
            runner.run(arguments, silent)
            mock_call.assert_called_once()
            assert isinstance(mock_call, mock.MagicMock)

            assert mock_call.call_args[0][0] == arguments

            if want_err:
                pytest.fail(f'expected an exception for status {status}.')  # pragma: nocover

    except OSError:
        if not want_err:
            pytest.fail(f'did not expect exception for status {status}.')  # pragma: nocover
