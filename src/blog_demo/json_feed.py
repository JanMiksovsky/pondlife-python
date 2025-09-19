from collections.abc import Mapping

from .site_info import site_info


def json_feed(posts: Mapping[str, Mapping]) -> dict:
    """Generate posts in JSON Feed format"""
    return {
        "version": "https://jsonfeed.org/version/1.1",
        "title": site_info["title"],
        "description": site_info["description"],
        "feed_url": f'{site_info["url"]}/feed.json',
        "home_page_url": site_info["url"],
        "items": [
            {
                "content_html": post["_body"].replace('src="/', f'src="{site_info["url"]}/'),
                "date_published": post["date"].isoformat(),
                "id": f'{site_info["url"]}/posts/{slug}',
                "title": post["title"],
                "url": f'{site_info["url"]}/posts/{slug}',
            }
            for slug, post in posts.items()
        ],
    }
