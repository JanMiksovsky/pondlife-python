"""
A "document" is just a dict with a `_body` property containing the main text
"""


import re

FRONT_MATTER_RE = re.compile(
    r"^\ufeff?---\s*\r?\n"         # opening --- (allow optional BOM)
    r"(?P<frontmatter>.*?)"        # front matter content (captured, named)
    r"\r?\n---\s*\r?\n?",          # closing ---
    re.DOTALL | re.MULTILINE,
)


def document(content: str | bytes) -> dict[str, str]:
    """
    Parse a text file with front matter delimited by lines of '---'. Front
    matter supports only 'key: value' per line (no nesting). Returns a dict of
    the keys plus '_body' with the remaining text.
    """
    text = content.decode("utf-8") if isinstance(content, bytes) else content
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
