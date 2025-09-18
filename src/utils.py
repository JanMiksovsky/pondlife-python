import inspect
import re
from collections.abc import Mapping
from typing import Callable

import markdown

FRONT_MATTER_RE = re.compile(
    r"^\ufeff?---\s*\r?\n"         # opening --- (allow optional BOM)
    r"(?P<frontmatter>.*?)"        # front matter content (captured, named)
    r"\r?\n---\s*\r?\n?",          # closing ---
    re.DOTALL | re.MULTILINE,
)


def add_next_previous(docs: dict) -> dict:
    """Add 'next_key' and 'previous_key' keys to each document in a dict of documents."""
    keys = list(docs.keys())
    extended = docs.copy()
    for i, key in enumerate(keys):
        doc = extended[key]
        doc['next_key'] = keys[i + 1] if i < len(keys) - 1 else None
        doc['previous_key'] = keys[i - 1] if i > 0 else None
    return extended


def fn_arity(fn: Callable) -> int:
    """
    Return the number of required positional-or-keyword parameters
    for the given function.
    
    Similar to JavaScript's Function.length.
    """
    sig = inspect.signature(fn)
    required = [
        p
        for p in sig.parameters.values()
        if p.default is inspect._empty
        and p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)
    ]
    return len(required)


def invoke_fns(m: Mapping) -> Mapping:
    """If a value in the mapping is a callable, call it with no arguments"""
    class InvokedMap(Mapping):
        def __getitem__(self, key):
            if key not in m:
                return None
            value = m[key]
            if callable(value):
                arity = fn_arity(value)
                if arity == 0:
                    return value()
                raise ValueError(f"Function for key '{key}' must take 0 arguments, but takes {arity}")
            return value

        def __iter__(self):
            yield from m

        def __len__(self):
            return len(m)

    return InvokedMap()
    

def map_items(d: Mapping, key=None, inverse_key=None, value=None):
    """
    Return a Mapping that transforms the keys and/or values of the given mapping.
    `key`: function that takes a source key and returns a result key
    `inverse_key`: function that takes a result key and returns the source key
    `value`: function that takes a source value and returns a result value
    """
    class TransformedMap(Mapping):
        def __getitem__(self, result_key):
            source_key = inverse_key(result_key) if inverse_key else result_key
            source_value = d[source_key]
            if value:
                arity = fn_arity(value)
                if arity == 2:
                    return value(source_value, source_key)
                if arity == 1:
                    return value(source_value)
                return value()
            return source_value

        def __iter__(self):
            for k in d:
                yield key(k) if key else k

        def __len__(self):
            return len(d)
        
    return TransformedMap()


def md_doc_to_html_doc(md_doc: dict) -> dict:
    """Convert the '_body' of a markdown document to HTML, returning a new document."""
    return {**md_doc, "_body": markdown.markdown(md_doc["_body"])}


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


def text_to_doc(input: str | bytes) -> dict[str, str]:
    """
    Parse a text file with simplistic front matter delimited by lines of '---'.
    Front matter supports only 'key: value' per line (no nesting).
    Returns a dict of the keys plus '_body' with the remaining text.
    """

    text = input.decode("utf-8") if isinstance(input, bytes) else input
    m = FRONT_MATTER_RE.match(text)
    result: dict[str, str] = {}

    if m:
        fm_text = m.group("frontmatter")   # use named capture
        # Parse key: value lines
        for line in fm_text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" in line:
                key, value = line.split(":", 1)
                result[key.strip()] = value.strip()

        body = text[m.end():]
        result["_body"] = body
    else:
        # No valid front matter — entire file is the body
        result["_body"] = text

    return result


def traverse_keys(d: Mapping, *args: str):
    """Use a set of keys to traverse a tree with dict nodes."""
    node = d
    for key in args:
        if node is None or not isinstance(node, Mapping):
            return None
        node = node.get(key)
    return node
