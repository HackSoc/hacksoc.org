
import os
from typing import Generator, List, cast
from hacksoc_org import root_dir, app

from flask_frozen import Freezer

freezer = Freezer(app)

def get_all_routes() -> List[str]:
    # not currently used
    routes = []

    for filename in os.listdir(os.path.join(root_dir, "templates", "content")):
        if filename.endswith(".html.jinja2"):
            routes.append("/" + filename.removesuffix(".jinja2"))

    for filename in os.listdir(os.path.join(root_dir, "templates", "content", "news")):
        routes.append("/news/" + filename.removesuffix(".html.jinja2").removesuffix(".md") + ".html")

    routes.extend(list(get_server_page_routes()))

    routes.extend(list(get_static_routes()))

    return routes


@freezer.register_generator
def get_static_routes() -> Generator[str]:
    top = os.path.join(root_dir, "static")
    for (dirpath, dirnames, filenames) in os.walk(top):
        for filename in filenames:
            route = '/static' +  dirpath.removeprefix(top) + '/' +  filename
            yield route

@freezer.register_generator
def get_server_page_routes() -> Generator[str]:
    for filename in os.listdir(os.path.join(root_dir, "templates", "content", "servers")):
        yield "/servers/" + filename.removesuffix(".html.jinja2").removesuffix(".md") + ".html"

def freeze():
    # https://pythonhosted.org/Frozen-Flask/#finding-urls
    # Currently flask_frozen will implicitly find routes (in our case) if there is a url_for call to them
    # Since none of the static assets are loaded like this, and the server pages are not linked to at all
    # from the main site, the two above generators provide routes for them
    # The unused get_all_routes() function can be adapted in the future if explicit route listing is desired.

    # this seemingly useless method is used to provide a stable API if the freeze provider changes in the future
    freezer.freeze()

if __name__ == "__main__":
    freeze()