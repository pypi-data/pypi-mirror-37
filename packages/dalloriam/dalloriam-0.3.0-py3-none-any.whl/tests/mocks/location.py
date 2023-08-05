from contextlib import contextmanager

@contextmanager
def mock_location(*args, **kwargs):
    yield 