from contextlib import contextmanager

import os


@contextmanager
def location(target_path: str) -> None:
    """
    Context manager that facilitates switching to a directory.
    Args:
        target_path: Path to switch to, temporarily.
    """
    old_path = os.getcwd()
    os.chdir(target_path)
    yield
    os.chdir(old_path)
