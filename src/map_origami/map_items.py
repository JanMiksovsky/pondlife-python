from typing import Mapping

from .utils import arity


def map_items(m: Mapping, key=None, inverse_key=None, value=None):
    """
    Return a Mapping that transforms the keys and/or values of the given mapping.
    `key`: function that takes a source key and returns a result key
    `inverse_key`: function that takes a result key and returns the source key
    `value`: function that takes a source value and returns a result value
    """
    class TransformedMap(Mapping):
        def __getitem__(self, result_key):
            source_key = inverse_key(result_key) if inverse_key else result_key
            source_value = m[source_key]
            if value:
                n = arity(value)
                if n == 3:
                    return value(source_value, source_key, m)
                if n == 2:
                    return value(source_value, source_key)
                if n == 1:
                    return value(source_value)
                return value()
            return source_value

        def __iter__(self):
            for k in m:
                yield key(k) if key else k

        def __len__(self):
            return len(m)

    return TransformedMap()
