from collections.abc import Mapping

from .map_items import map_items


def map_extensions(m: Mapping, extensions: str, value=None):
    """
    Return a Mapping that transforms the extensions of the keys, and optionally
    the values, of the given mapping.

    The `extension` should be a string of the form ".old->.new". Either the old
    or new extension can be empty to indicate no extension.
    """
    if "->" not in extensions:
        raise ValueError("extensions must be of the form .old->.new")
    old_ext, new_ext = extensions.split("->", 1)

    def key(source_key):
        if source_key.endswith(old_ext):
            return source_key[:len(source_key) - len(old_ext)] + new_ext
        return source_key

    def inverse_key(result_key):
        if result_key.endswith(new_ext):
            return result_key[:len(result_key) - len(new_ext)] + old_ext
        return result_key

    return map_items(m, key=key, inverse_key=inverse_key, value=value)
