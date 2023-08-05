from flask import request

from functools import wraps


def authenticated(password):
    def decorator(fn):
        @wraps(fn)
        def internal(*args, **kwargs):
            expected = request.headers.get('Authorization', 'secret')
            if expected == password:
                return fn(*args, **kwargs)
            else:
                raise ValueError('forbidden')

        return internal

    return decorator