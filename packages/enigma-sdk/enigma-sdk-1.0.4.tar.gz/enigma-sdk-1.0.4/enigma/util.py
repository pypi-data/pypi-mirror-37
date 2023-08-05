"""Miscellaneous utility functions."""
import functools


def adjust_kwargs(func, defaults={}, listify=()):
    """Return a function that decorates the kwarg-handling behavior of *func*.

    Arguments in the *defaults* dict will be added to each call when not present.
    Arguments named in the *listify* collection will be converted to list if needed.
    """
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        for kw, value in defaults.items():
            if kw not in kwargs:
                kwargs[kw] = value
        for name in listify:
            if name in kwargs:
                value = kwargs[name]
                if not isinstance(value, list):
                    kwargs[name] = [value]
        return func(*args, **kwargs)
    return wrapped
