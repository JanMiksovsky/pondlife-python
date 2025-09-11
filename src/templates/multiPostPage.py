from ..siteInfo import siteInfo
from .page import page
from .postFragment import postFragment


def multiPostPage(posts):
    """Base page template for all pages"""
    postFragments = [postFragment(post, key) for key, post in posts.items()]
    return page({
        "title": siteInfo["title"],
        "area": "home",
        "_body": f"""\
          <h1>{siteInfo["title"]}</h1>
          <p>{siteInfo["description"]}</p>
          {"".join(postFragments)}
          <footer>
            <a href="/feed.xml">RSS feed</a>
            <a href="/feed.json">JSON feed</a>
            <a href="https://github.com/WebOrigami/pondlife-zero-deps">View source</a>
          </footer>
        """
    })
