from typing import Mapping


def add_next_previous(docs: Mapping):
    """
    Given a mapping of documents, return a new mapping where each document has
    'next_key' and 'previous_key' fields added, pointing to the keys of the
    next and previous documents in the original mapping's order. If there is no
    next or previous document, the corresponding field is None.
    """
    keys = list(docs.keys())

    class DocsWithNextPrevious(Mapping):
        def __getitem__(self, key):
            if key not in docs:
                raise KeyError(key)
            i = keys.index(key)
            return {
                **docs[key],
                "next_key": keys[i + 1] if i < len(keys) - 1 else None,
                "previous_key": keys[i - 1] if i > 0 else None,
            }

        def __iter__(self):
            yield from docs

        def __len__(self):
            return len(docs)
    return DocsWithNextPrevious()
