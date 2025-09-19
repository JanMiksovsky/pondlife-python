from ..site_info import site_info
from .page import page
from .post_fragment import post_fragment


def multi_post_page(paginated):
    """Base page template for all pages"""
    items = paginated["items"]
    next_page = paginated["next_page"]
    previous_page = paginated["previous_page"]
    page_number = paginated["page"]
    postFragments = [post_fragment(post, key) for key, post in items.items()]
    return page({
        "title": site_info["title"],
        "area": "home" if page_number == 1 else None,
        "_body": f"""\
          <h1>{site_info["title"]}</h1>
          <p>{site_info["description"]}</p>
          {"".join(postFragments)}
          <p>
            {f"""
              <a class="next" href="/pages/{next_page}.html"><strong>Older posts</strong></a>
              <span>&nbsp;</span>
            """ if next_page else ""
            }
            {f"""
              <a class="previous" href="{"/" if previous_page == 1 else f"/pages/{previous_page}.html"}"><strong>Newer posts</strong></a>
            """ if previous_page else ""
            }
          </p>
            <footer>
            <a href="/feed.xml">RSS feed</a>
            <a href="/feed.json">JSON feed</a>
            <a href="https://github.com/JanMiksovsky/pondlife-python">View source</a>
          </footer>
        """
    })
