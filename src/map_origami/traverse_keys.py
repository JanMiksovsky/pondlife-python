from collections.abc import Mapping
from typing import Any


def traverse_keys(m: Mapping, *args: str):
    """Use a set of keys to traverse a tree with Mapping nodes."""
    result: Any = m
    for key in args:
        if result is None or not isinstance(result, Mapping):
            return None
        result = result.get(key)
    return result
