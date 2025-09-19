from .page import page
from .post_fragment import post_fragment


def single_post_page(post, key, post_docs):
    """Base page template for all pages"""
    next_key = post["next_key"]
    previous_key = post["previous_key"]
    return page({
        "title": post["title"],
        "_body": f"""
          {post_fragment(post, key)}
          <p>
              {f"""
                  <a class="previous" href="{previous_key}">
                      Previous: {post_docs[previous_key]["title"]}
                  </a>
                  &nbsp;
                """ if previous_key else ""}
              {f"""
                  <a class="next" href="{next_key}">
                  Next: {post_docs[next_key]["title"]}
                  </a>
                """
                if next_key
                else f"""
                  <a class="next" href="/">
                      Back to home
                  </a>
                """}
          </p>
        """
    })
