from datetime import datetime, timezone
from typing import Any, Dict, Iterable, Optional
from urllib.parse import urlparse


def json_feed_to_rss(json_feed: Dict[str, Any], options: Optional[Dict[str, Any]] = None) -> str:
    """
    Convert a JSON Feed (https://jsonfeed.org/version/1) object to RSS 2.0 XML text.
    `options` may contain: feed_url, language.
    """
    options = options or {}

    description: Optional[str] = json_feed.get("description")
    home_page_url: Optional[str] = json_feed.get("home_page_url")
    items: Iterable[Dict[str, Any]] = json_feed.get("items", []) or []
    title: Optional[str] = json_feed.get("title")

    feed_url: Optional[str] = options.get("feed_url")
    language: Optional[str] = options.get("language")

    if not feed_url and json_feed.get("feed_url"):
        # Presume RSS sits next to the JSON feed with a .xml extension.
        feed_url = str(json_feed["feed_url"])
        if feed_url.endswith(".json"):
            feed_url = feed_url[:-5] + ".xml"

    items_rss = "".join(item_rss(story) for story in items)

    title_el = f"    <title>{escape_xml(title)}</title>\n" if title else ""
    desc_el = f"    <description>{escape_xml(description)}</description>\n" if description else ""
    link_el = f"    <link>{home_page_url}</link>\n" if home_page_url else ""
    lang_el = f"    <language>{language}</language>\n" if language else ""
    feed_link_el = (
        f'    <atom:link href="{feed_url}" rel="self" type="application/rss+xml"/>\n'
        if feed_url
        else ""
    )

    return (
        '<?xml version="1.0" ?>\n'
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" '
        'xmlns:content="http://purl.org/rss/1.0/modules/content/">\n'
        "  <channel>\n"
        f"{title_el}{desc_el}{link_el}{lang_el}{feed_link_el}{items_rss}"
        "  </channel>\n"
        "</rss>"
    )


def item_rss(item: Dict[str, Any]) -> str:
    content_html: Optional[str] = item.get("content_html")
    item_id: Optional[str] = item.get("id")
    summary: Optional[str] = item.get("summary")
    title: Optional[str] = item.get("title")
    url: Optional[str] = item.get("url")

    date_published = item.get("date_published")
    # Accept ISO 8601 strings (including 'Z'), datetime objects, or None.
    if isinstance(date_published, str):
        date_published = parse_iso8601(date_published)

    if isinstance(date_published, datetime):
        pub_date = to_rfc822_date(date_published)
    else:
        pub_date = None

    date_el = f"      <pubDate>{pub_date}</pubDate>\n" if pub_date else ""
    is_perma_link_attr = ' isPermaLink="false"' if (item_id is not None and not is_absolute_url(str(item_id))) else ""
    guid_el = f"      <guid{is_perma_link_attr}>{item_id}</guid>\n" if item_id else ""
    desc_el = f"      <description>{escape_xml(summary)}</description>\n" if summary else ""
    content_el = f"      <content:encoded><![CDATA[{content_html}]]></content:encoded>\n" if content_html else ""
    title_el = f"      <title>{escape_xml(title)}</title>\n" if title else ""
    link_el = f"      <link>{url}</link>\n" if url else ""

    return (
        "    <item>\n"
        f"{date_el}{title_el}{link_el}{guid_el}{desc_el}{content_el}"
        "    </item>\n"
    )


def escape_xml(text: Optional[str]) -> str:
    """Escape XML entities in text content."""
    if text is None:
        return ""
    # Order matters: ampersand first to avoid double-escaping.
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&apos;")
    )


def parse_iso8601(s: str) -> datetime:
    """Parse an ISO-8601 datetime string, accepting a trailing 'Z' for UTC."""
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    # fromisoformat handles most RFC 3339/ISO-8601 forms.
    dt = datetime.fromisoformat(s)
    # Ensure timezone-aware; assume UTC if naive.
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def to_rfc822_date(dt: datetime) -> str:
    """Format a datetime as RFC-822 (RFC-2822) with GMT, matching your JS output."""
    dt_utc = dt.astimezone(timezone.utc)
    # Example: "Thu, 11 Sep 2025 00:00:00 GMT"
    return dt_utc.strftime("%a, %d %b %Y %H:%M:%S GMT")


def is_absolute_url(s: str) -> bool:
    """Rough equivalent of URL.canParse: absolute URL with scheme and netloc."""
    u = urlparse(s)
    return bool(u.scheme and u.netloc)
