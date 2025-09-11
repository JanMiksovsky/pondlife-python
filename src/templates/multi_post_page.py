from ..site_info import site_info
from .page import page
from .post_fragment import post_fragment


def multi_post_page(posts):
    """Base page template for all pages"""
    postFragments = [post_fragment(post, key) for key, post in posts.items()]
    return page({
        "title": site_info["title"],
        "area": "home",
        "_body": f"""\
          <h1>{site_info["title"]}</h1>
          <p>{site_info["description"]}</p>
          {"".join(postFragments)}
          <footer>
            <a href="/feed.xml">RSS feed</a>
            <a href="/feed.json">JSON feed</a>
            <a href="https://github.com/WebOrigami/pondlife-zero-deps">View source</a>
          </footer>
        """
    })
