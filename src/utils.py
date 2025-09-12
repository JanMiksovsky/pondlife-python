import re
from pathlib import Path

import markdown

FRONT_MATTER_RE = re.compile(
    r"^\ufeff?---\s*\r?\n"         # opening --- (allow optional BOM)
    r"(?P<frontmatter>.*?)"        # front matter content (captured, named)
    r"\r?\n---\s*\r?\n?",          # closing ---
    re.DOTALL | re.MULTILINE,
)

def document_dict(input: str | bytes) -> dict[str, str]:
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

def md_doc_to_html_doc(md_doc: dict) -> dict:
    """Convert the '_body' of a markdown document dict to HTML, returning a new dict."""
    return {**md_doc, "_body": markdown.markdown(md_doc["_body"])}

def paginate(docs: dict, size: int = 10) -> list[dict]:
    """Split a dict of documents into a list of dicts, each with up to size items."""
    items = list(docs.items())
    pages = [{
            "items": dict(items[i:i + size]),
            "next_page": (i + size) // size + 1 if i + size < len(items) else None,
            "page": i // size + 1,
            "page_count": (len(items) + size - 1) // size,
            "previous_page": i // size if i > 0 else None,
         } for i in range(0, len(items), size)]
    return pages
