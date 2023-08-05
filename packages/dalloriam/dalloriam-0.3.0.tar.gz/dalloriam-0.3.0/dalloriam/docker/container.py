from dalloriam.shell import run

from typing import Iterable, Dict

import random
import string


def _random_name(size: int = 12) -> str:
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=size))


class Container:

    def __init__(self, image_name: str, tag: str) -> None:
        self.name = f'{image_name}-{_random_name()}'
        self._image = f'{image_name}:{tag}'

    def start(self, ports: Dict[int, int] = None, volumes: Dict[str, str] = None) -> None:
        """
        Starts the container.
        Args:
            ports: The port mappings.
            volumes: The volume mappings.
        """
        ports_lst = []
        if ports is not None:
            for k, v in ports.items():
                ports_lst.append('-p')
                ports_lst.append(f'{k}:{v}')

        vol_lst = []
        if volumes is not None:
            for k, v in volumes.items():
                vol_lst.append('-v')
                vol_lst.append(f'{k}:{v}')

        run([
            'docker',
            'run',
            '--rm',
            '-d',
            *ports_lst,
            *vol_lst,
            '--name',
            self.name,
            self._image
        ], silent=True)

    def stop(self) -> None:
        """
        Stops the container.
        """
        run([
            'docker',
            'stop',
            self.name
        ], silent=True)

    def exec(self, cmd: Iterable[str], background: bool = False) -> None:
        """
        Executes a command inside the container
        Args:
            cmd: The command arguments.
            background: Whether to execute the command in the background or to await the results.
        """
        run([
            'docker',
            'exec',
            '-d' if background else '-i',
            self.name,
            *cmd
        ], silent=False)
