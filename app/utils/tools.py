import logging
import traceback

from collections.abc import Iterable
from django.utils.module_loading import import_string

from app.settings import TESTING


def coerce_list(target) -> list:
    """Take a given input and convert it to a list."""
    if isinstance(target, Iterable) and not isinstance(target, str):
        return list(target)
    elif target is None:
        return []
    else:
        return [target]


def is_not_empty(target) -> bool:
    """Determines if a value is not None or an empty list."""
    return (
        target is not None
        and not (isinstance(target, list) and len(target) == 0)
        and not (isinstance(target, str) and target == "")
    )


def print_error():
    """Log an error with stacktrace that's been handled via try/except."""
    if TESTING:
        return

    tb = traceback.format_exc()
    logging.warn(tb)


def get_import_path(symbol):
    """
    Get a string version of class or function to be imported by
    a celery task or other thread operation.

    Parameters
    ----------
        - symbol (class, callable): The class, function, or other object to get import string of.

    Example
    -------
    ```
    # file_one.py
    class Something:
        pass

    obj_path = get_import_path(Something)

    # file_two.py
    Something = import_from_path(obj_path)
    ```
    """

    return f"{symbol.__module__}.{symbol.__qualname__}"


def import_from_path(path: str):
    """
    Get a symbol from its import path.

    Reverse function for `get_import_path`.
    Wraps django's default `import_string` function.
    """

    return import_string(path)


def clean_list(target: list):
    """Remove None values and empty strings from list."""

    return [item for item in target if item is not None and item != ""]
