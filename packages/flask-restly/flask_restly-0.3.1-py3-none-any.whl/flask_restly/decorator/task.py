from functools import wraps
from uuid import uuid4
from flask import copy_current_request_context, jsonify


def task():
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            task_id = uuid4().hex

            @copy_current_request_context
            def task():
                try:
                    data = f(*args, **kwargs)
                except:
                    redis.set(skey, 500)
                else:
                    redis.set(skey, 200)
                    redis.set(key, data)
                    redis.expire(key, expire_time)
                redis.expire(skey, expire_time)

            return jsonify({"id": task_id})
        return wrapper
    return decorator
