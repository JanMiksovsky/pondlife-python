from pathlib import Path

from jinja2 import DictLoader, Environment

from map_origami import Folder, map_extensions, map_items

from .site_info import site_info

here = Path(__file__).parent
template_folder = Folder(here / "templates")
template_texts = map_items(
    template_folder,
    value=lambda content: content.decode(
        "utf-8") if isinstance(content, bytes) else content
)
env = Environment(loader=DictLoader(template_texts))
env.globals["site_info"] = site_info


def template_fn(content, template_name):
    """Return a function that renders the given template with a context"""
    template = env.get_template(template_name)
    return lambda value, key, map: template.render(value=value, key=key, map=map)


# Create a template function for each template file
templates = map_extensions(
    template_texts, extensions=".j2->", value=template_fn
)
