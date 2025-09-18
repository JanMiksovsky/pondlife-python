from collections.abc import Mapping

from .utils import transform_dict


class GreetMap(Mapping):
    names = "Alice", "Bob", "Carol"

    def __getitem__(self, key):
        if key in self.names:
            return f"Hello, {key}!"
        raise KeyError(key)

    def __iter__(self):
        yield from self.names

    def __len__(self):
        return len(self.names)

m = GreetMap()
upper_map = transform_dict(m, value=str.upper)
print(list(m.items()))
print(list(upper_map.items()))
