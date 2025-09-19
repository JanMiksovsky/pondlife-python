
from collections.abc import Mapping

from .utils import arity


def invoke_fns(m: Mapping) -> Mapping:
    """If a value in the mapping is a callable, call it with no arguments"""
    class InvokedMap(Mapping):
        def __getitem__(self, key):
            if key not in m:
                return None
            value = m[key]
            if callable(value):
                n = arity(value)
                if n == 0:
                    return value()
                raise ValueError(
                    f"Function for key '{key}' must take 0 arguments, but takes {n}")
            return value

        def __iter__(self):
            yield from m

        def __len__(self):
            return len(m)

    return InvokedMap()
