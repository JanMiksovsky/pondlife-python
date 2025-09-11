def post_fragment(post, key):
    """A single blog post, on its own or in a list"""
    return f"""\
<section>
  <a href="/posts/{key}">
    <h2>{post["title"]}</h2>
  </a>
  {post["date"].strftime("%B %-d, %Y")}
  {post["_body"]}
</section>
"""
