"""
Memoizing
Code is from <<Expert Python Programming>> (Second Edition, Michal Jaworski).
Visit: 'https://en.wikipedia.org/wiki/Memoization' for more information.
"""
import hashlib
import pickle
import time

cache = {}


def _is_obsolete(entry, duration):
    return time.time() - entry['time'] > duration


def _compute_key(function, args, kwargs):
    key = pickle.dumps((function.__name__, args, kwargs))
    return hashlib.sha1(key).hexdigest()


def memoize(duration=10):
    def _memoize(function):
        def __memoize(*args, **kwargs):
            key = _compute_key(function, args, kwargs)

            if (key in cache) and (not _is_obsolete(cache[key], duration)):
                return cache[key]['value']

            result = function(*args, **kwargs)

            cache[key] = {
                'value': result,
                'time': time.time()
            }
            return result
        return __memoize
    return _memoize
