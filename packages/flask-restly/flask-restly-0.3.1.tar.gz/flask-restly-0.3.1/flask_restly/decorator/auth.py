from functools import wraps
from flask_restly._storage import append_skip_authorization
from flask import current_app


def unauthorized(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    append_skip_authorization(wrapper)

    return wrapper


def provider(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    current_app.extensions.get('rest-api').set_auth_provider(wrapper)

    return wrapper
