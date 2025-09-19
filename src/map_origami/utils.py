"""
Utility functions
"""

import inspect
from collections.abc import Callable


def arity(fn: Callable) -> int:
    """Number of a function's required positional or keyword parameters"""
    sig = inspect.signature(fn)
    required = [
        p
        for p in sig.parameters.values()
        if p.default is inspect._empty
        and p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)
    ]
    return len(required)
