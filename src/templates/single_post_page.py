from .page import page
from .post_fragment import post_fragment


def single_post_page(post, key):
    """Base page template for all pages"""
    return page({
        "title": post["title"],
        "_body": post_fragment(post, key)
    })