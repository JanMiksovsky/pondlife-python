from collections.abc import Mapping


def paginate(docs: Mapping, size: int = 10) -> list[dict]:
    """Split a set of documents into a list of dicts, each with up to `size` items."""
    items = list(docs.items())
    pages = [{
        "items": dict(items[i:i + size]),
        "next_page": (i + size) // size + 1 if i + size < len(items) else None,
        "page": i // size + 1,
        "page_count": (len(items) + size - 1) // size,
        "previous_page": i // size if i > 0 else None,
    } for i in range(0, len(items), size)]
    return pages
