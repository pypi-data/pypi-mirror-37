from dalloriam import docker

from tests.mocks.location import mock_location

from unittest import mock


@mock.patch.object(docker.client.DockerClient, '_login')
def test_client_init_calls_login_when_required(mock_login: mock.MagicMock):

    docker.Client()

    mock_login.assert_not_called()

    docker.Client(server='some/custom/server')

    mock_login.assert_called_once()
    mock_login.reset_mock()

    docker.Client(username='hello')
    mock_login.assert_not_called()

    docker.Client(username='hello', password='world')
    mock_login.assert_called_once()


def test_client_build_calls_shell_run_properly():
    client = docker.Client()

    with mock.patch.object(docker.client.filesystem, 'location', mock_location),\
             mock.patch.object(docker.client.shell, 'run') as mock_run:
        client.build('some_path', 'my_image', 'mytag')
        mock_run.assert_called_once()

        mock_run.assert_called_with(['docker', 'build', '-t', 'my_image:mytag', '.'], silent=True)


def test_client_build_sets_default_tag():
    client = docker.Client()

    with mock.patch.object(docker.client.filesystem, 'location', mock_location), \
            mock.patch.object(docker.client.shell, 'run') as mock_run:
        client.build('some_path', 'my_image')
        mock_run.assert_called_once()

        mock_run.assert_called_with(['docker', 'build', '-t', 'my_image:latest', '.'], silent=True)


def test_client_push_calls_correct_command():
    client = docker.Client()

    with mock.patch.object(docker.client.shell, 'run') as mock_run:
        client.push('someuser/some_image', 'some_tag')
        mock_run.assert_called_once()

        mock_run.assert_called_with(['docker', 'push', 'someuser/some_image:some_tag'], silent=False)


def test_client_container_initializes_container_correctly():
    client = docker.Client()

    port_data = {32: 32}
    vol_data = {'vol': 'vol'}

    with mock.patch.object(docker.client.Container, 'start') as mock_start, \
            mock.patch.object(docker.client.Container, 'stop') as mock_stop:

        with client.container('some_image', 'some_tag', ports=port_data, volumes=vol_data) as c:
            assert isinstance(c, docker.Container)
            assert c.name.startswith('some_image') and c.name != 'some_image'
            mock_start.assert_called_once_with(port_data, vol_data)
            mock_stop.assert_not_called()

        mock_stop.assert_called_once()
