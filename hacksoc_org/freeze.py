
import os
from typing import cast
from hacksoc_org import root_dir, app

from flask_frozen import Freezer

freezer = Freezer(app)

def get_all_routes():
    # not used because flask_frozen finds all pages refered by url_for

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
def get_static_routes():
    top = os.path.join(root_dir, "static")
    for (dirpath, dirnames, filenames) in os.walk(top):
        for filename in filenames:
            route = '/static' +  dirpath.removeprefix(top) + '/' +  filename
            yield route

@freezer.register_generator
def get_server_page_routes():
    for filename in os.listdir(os.path.join(root_dir, "templates", "content", "servers")):
        yield "/servers/" + filename.removesuffix(".html.jinja2").removesuffix(".md") + ".html"

if __name__ == "__main__":
    freezer.freeze()