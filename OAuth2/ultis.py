from functools import wraps
from flask import session, redirect


def login_required(f):
    @wraps(f)
    def _decorator_func(*args, **kwargs):
        user = dict(session).get('profile', None)
        if user:
            return f(*args, **kwargs)
        return redirect('/auth/login')

    return _decorator_func
