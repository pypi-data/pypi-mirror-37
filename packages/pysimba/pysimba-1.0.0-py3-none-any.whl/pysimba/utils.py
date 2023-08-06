from functools import wraps
from itertools import chain
from datetime import datetime
from delorean import Delorean


def chunks(items, n):
    for i in range(0, len(items), n):
        yield items[i:i+n]


def get(data, path, default=None):
    _data = data
    for x in path.split('.'):
        try:
            _data = _data[x]
        except KeyError:
            if default:
                return default
            else:
                raise
    return _data


def deep_dict(data, path):
    _data = data
    for x in reversed(path.split('.')):
        _data = {x: _data}
    return _data


def batch(n, path=None, default=None):
    """
    Batch lets you divide an iterable (currently, last positional argument) of work into pieces.
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            _args = list(args)
            target = _args.pop()
            R = [f(*_args, x, **kwargs) for x in chunks(target, n=n)]
            r = chain(*R)
            return list(r)
        return wrapper
    return decorator


def strptime(date_string):
    return Delorean(datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S'), timezone='Asia/Shanghai').datetime
