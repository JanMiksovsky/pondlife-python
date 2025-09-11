from .page import page
from .postFragment import postFragment


def multiPostPage(posts):
    """Base page template for all pages"""
    postFragments = [postFragment(post, key) for key, post in posts.items()]
    return page({
        "title": "#pondlife",
        "_body": f"""\
          <h1>#pondlife</h1>
          <p>https://pondlife-zero-deps.netlify.app</p>
          {"".join(postFragments)}
          <footer>
            <a href="/feed.xml">RSS feed</a>
            <a href="/feed.json">JSON feed</a>
            <a href="https://github.com/WebOrigami/pondlife-zero-deps">View source</a>
          </footer>
        """
    })
