"""
A folder of Jinja2 templates mapped to functions that apply those templates.
"""

from pathlib import Path

from jinja2 import DictLoader, Environment

from map_origami import Folder, map_extensions, map_items

from .site_info import site_info

# Create a loader for the folder. Could also use FileSystemLoader, but we
# already want to treat the folder as a map.
here = Path(__file__).parent
folder = Folder(here / "templates")
texts = map_items(folder, value=lambda b: b.decode("utf-8"))
env = Environment(loader=DictLoader(texts))

# Give templates access to site information
env.globals["site_info"] = site_info


def template_fn(content, template_name):
    """Return a function that renders the given template"""
    # Instead of using the supplied content, we use the loader so that it can
    # handle includes and extends.
    template = env.get_template(template_name)
    return lambda value, key, map: template.render(value=value, key=key, map=map)


# Create a template function for each template file
templates = map_extensions(
    texts, extensions=".j2->", value=template_fn
)
