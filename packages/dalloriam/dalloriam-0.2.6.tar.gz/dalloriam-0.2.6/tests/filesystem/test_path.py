from dalloriam.filesystem import path

from unittest import mock


def test_location_context_manager():
    mock_dir = 'hello'
    with mock.patch.object(path.os, 'getcwd', return_value=mock_dir), \
            mock.patch.object(path.os, 'chdir') as mock_chdir:

        with path.location('some_path'):
            mock_chdir.assert_called_with('some_path')

        mock_chdir.assert_called_with(mock_dir)
