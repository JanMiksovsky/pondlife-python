def postFragment(post, key):
    """A single blog post, on its own or in a list"""
    return f"""\
<section>
  <a href="/posts/{key}">
    <h2>{post["title"]}</h2>
  </a>
  {post["_body"]}
</section>
"""
