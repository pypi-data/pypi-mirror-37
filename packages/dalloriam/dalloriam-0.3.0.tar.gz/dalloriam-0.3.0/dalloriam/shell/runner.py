from subprocess import call

from typing import List

import os


def run(cmd_args: List[str], silent=True) -> None:
    """
    Run a shell command with it's arguments.
    Args:
        cmd_args:  The command & arguments.
        silent: Whether to swallow the output.
    """

    if silent:
        with open(os.devnull, 'w') as fnull:
            status = call(cmd_args, stdout=fnull)
    else:
        status = call(cmd_args)

    if status != 0:
        # TODO: Retrieve cmd stdout/stderr
        raise OSError(f"an error ({status})  occured while running command {cmd_args[0]}")
