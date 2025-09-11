from .page import page
from .postFragment import postFragment


def singlePostPage(data, key):
    """Base page template for all pages"""
    return page({
        "title": data["title"],
        "_body": postFragment(data, key)
    })