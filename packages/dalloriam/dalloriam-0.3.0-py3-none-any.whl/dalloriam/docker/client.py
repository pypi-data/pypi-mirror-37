from contextlib import contextmanager

from dalloriam import filesystem, shell
from dalloriam.docker.container import Container

from typing import Dict, Iterator

import os
import random
import string
import time


class DockerClient:

    def __init__(self, username: str = None, password: str = None, server: str = None) -> None:
        """
        Initializes the client
        Args:
            username: Docker repository username.
            password: Docker repository password.
            server: Docker repository URL.
        """
        self._username = username
        self._password = password
        self._server = server

        if (self._username and self._password) or self._server:
            self._login()

    @staticmethod
    def _format_image_name(image_name: str, tag: str) -> str:
        return f'{image_name}:{tag}'

    @staticmethod
    def _generate_random_name(length: int = 12) -> str:
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    def _login(self) -> None:
        args = [
            'docker',
            'login'
        ]

        if self._username:
            args += ['-u', self._username]

        if self._password:
            args += ['-p', self._password]

        if self._server:
            args.append(self._server)

        shell.run(args, silent=False)

    def build(self, content_dir: str, image_name: str, tag: str = 'latest') -> None:
        """
        Builds a docker image from a directory.
        Args:
            content_dir: Path that contains the image-related files.
            image_name: Desired name of the built image.
            tag:        Desired tag of the built image.
        """
        with filesystem.location(os.path.abspath(content_dir)):
            shell.run([
                'docker',
                'build',
                '-t',
                self._format_image_name(image_name, tag),
                '.'
            ], silent=True)

    def push(self, image_name: str, tag: str = 'latest') -> None:
        """
        Pushes a docker image to the target repository
        Args:
            image_name: Name of the image to push.
            tag: Tag of the image.
        """
        shell.run([
            'docker',
            'push',
            self._format_image_name(image_name, tag)
        ], silent=False)

    @contextmanager
    def container(
            self,
            image_name: str,
            tag: str = 'latest',
            ports: Dict[int, int] = None,
            volumes: Dict[str, str] = None) -> Iterator[Container]:
        """
        Start a container with the specified configuration in a context.
        Args:
            image_name: Name of the image to start.
            tag: Tag of the image to start.
            ports: Port mappings.
            volumes: Volume mappings.

        Returns:
            Running container.
        """
        c = Container(image_name=image_name, tag=tag)
        c.start(ports, volumes)
        time.sleep(2)
        yield c
        c.stop()
