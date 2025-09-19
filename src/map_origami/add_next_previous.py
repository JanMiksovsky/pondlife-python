from typing import Mapping


def add_next_previous(docs: Mapping) -> dict:
    keys = list(docs.keys())
    return {
        key: {
            **docs[key],
            "next_key": keys[i + 1] if i < len(keys) - 1 else None,
            "previous_key": keys[i - 1] if i > 0 else None,
        }
        for i, key in enumerate(keys)
    }
