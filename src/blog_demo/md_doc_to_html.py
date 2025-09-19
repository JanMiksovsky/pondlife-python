import re

import markdown

FRONT_MATTER_RE = re.compile(
    r"^\ufeff?---\s*\r?\n"         # opening --- (allow optional BOM)
    r"(?P<frontmatter>.*?)"        # front matter content (captured, named)
    r"\r?\n---\s*\r?\n?",          # closing ---
    re.DOTALL | re.MULTILINE,
)


def md_doc_to_html(md_doc: dict) -> dict:
    """Convert the '_body' of a markdown document to HTML, returning a new document."""
    return {**md_doc, "_body": markdown.markdown(md_doc["_body"])}
