from collections.abc import Mapping


def paginate(docs: Mapping, size: int = 10) -> Mapping[dict]:
    """
    Split a set of documents into a set of dicts, each with up to `size` items.
    The keys will be numbers (from 1 to the number of pages - 1) as strings to
    make it easier to use them as file names.
    """
    items = list(docs.items())
    page_count = (len(items) + size - 1) // size  # 1-based
    if page_count == 0:
        return {}
    return {
        str(i): {
            "items": items[(i - 1) * size: i * size],
            "next_page": str(i + 1) if i < page_count else None,
            "page": i,
            "page_count": page_count,
            "previous_page": str(i - 1) if i > 1 else None,
        } for i in range(1, page_count + 1)
    }
