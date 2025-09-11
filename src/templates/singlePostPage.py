from .page import page
from .postFragment import postFragment


def singlePostPage(post, key):
    """Base page template for all pages"""
    return page({
        "title": post["title"],
        "_body": postFragment(post, key)
    })