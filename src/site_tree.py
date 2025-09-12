import json
from pathlib import Path

from .files import readFiles
from .json_feed import json_feed
from .json_feed_to_rss import json_feed_to_rss
from .post_docs import post_docs
from .templates.multi_post_page import multi_post_page
from .templates.page import page
from .templates.single_post_page import single_post_page
from .utils import document_dict, md_doc_to_html_doc

# About page
here = Path(__file__).parent
about_path = here / "about.md"
about_md = about_path.read_text(encoding="utf-8")
about_md_doc = document_dict(about_md)
about_html_doc = md_doc_to_html_doc(about_md_doc)
about_page = page(about_html_doc)

# Assets
assets = readFiles(here / "assets")

# Feeds
feed = json_feed(post_docs)
feed_json = json.dumps(feed, indent=2)
rss_xml = json_feed_to_rss(feed)

# Static images
images = readFiles("images")

# Index page
index_page = multi_post_page(post_docs)

# Posts area
post_pages = {
    key: single_post_page(document, key)
    for key, document in post_docs.items()
}

site_tree = {
    "about.html": about_page,
    "assets": assets,
    "feed.json": feed_json,
    "feed.xml": rss_xml,
    "images": images,
    "index.html": index_page,
    "posts": post_pages,
}
