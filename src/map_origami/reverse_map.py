from collections.abc import Mapping


def reverse_map(m: Mapping) -> Mapping:
    """Return a new mapping that lazily reverses the keys."""
    class ReversedMap(Mapping):
        def __getitem__(self, key):
            return m.get(key)

        def __iter__(self):
            return reversed(list(m.keys()))

        def __len__(self):
            return len(m)

    return ReversedMap()
