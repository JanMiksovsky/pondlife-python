def page(data):
    """Base page template for all pages"""
    return f"""\
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" type="text/css" href="/assets/styles.css">
    <link rel="alternate" type="application/rss+xml" title="Dispatches from off the grid" href="/feed.xml">
    <link rel="alternate" type="application/json" title="Dispatches from off the grid" href="/feed.json">
    <title>{data["title"]}</title>
  </head>
  <body {"class=\"{data[\"area\"]}\"" if "area" in data else ""}>
    <header>
      <a href="/" class="home">#pondlife</a>
      <a href="/about.html" class="about">About</a>
    </header>
    <main>    
{data["_body"]}
    </main>
  </body>
</html>
"""
