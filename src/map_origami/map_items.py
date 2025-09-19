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
            if not value:
                return source_value
            # We can pass the source value, key, and the whole map
            params = [source_value, source_key, m]
            # Trim to pass only as many parameters as the value function wants
            params = params[:max(0, arity(value))]
            result_value = value(*params)
            return result_value

        def __iter__(self):
            for source_key in m:
                result_key = key(source_key) if key else source_key
                yield result_key

        def __len__(self):
            return len(m)

    return TransformedMap()
