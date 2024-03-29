"""
    Calls all URL routes, saves them to HTML files, and copies static files into
    `build/` suitable for serving from a static HTTP server
"""

import os
from typing import Generator, List
from hacksoc_org import ROOT_DIR, app

from hacksoc_org.util import removesuffix, removeprefix

from flask_frozen import Freezer

# flask_frozen config is done on the `app` object in __init__.py
freezer = Freezer(app)


def get_all_routes() -> List[str]:
    """Provided for future contingency but currently unused; explicitly provides
    a list of all URL routes (including static routes) that flask_frozen can
    call without relying on discovery via url_for

    Returns:
        List[str]: URL routes
    """
    # not currently used
    routes = []

    for filename in os.listdir(os.path.join(ROOT_DIR, "templates", "content")):
        if filename.endswith((".html.jinja2", ".xml.jinja2")):
            routes.append("/" + removesuffix(filename, ".jinja2"))

    for filename in os.listdir(os.path.join(ROOT_DIR, "templates", "content", "news")):
        routes.append(
            "/news/" + removesuffix(removesuffix(filename, ".html.jinja2"), ".md") + ".html"
        )

    routes.extend(list(get_server_page_routes()))

    routes.extend(list(get_static_routes()))

    return routes


@freezer.register_generator
def get_static_routes() -> Generator[str, None, None]:
    """Yields URL routes for every file in static/, whether it's used in the site or not. The site
    templates (currently) don't use url_for for static assets, and static assets may be used for
    off-site purposes, so it's better to be explicit in this case.

    Yields:
        Generator[str, None, None]: URL routes for static assets
    """
    top = os.path.join(ROOT_DIR, "static")
    for (dirpath, _, filenames) in os.walk(top):
        for filename in filenames:
            route = "/static" + removeprefix(dirpath, top).replace(os.sep, "/") + "/" + filename
            # `filename` is an OS-specific path (using `os.sep`); output is a URL route (using /)
            yield route


@freezer.register_generator
def get_server_page_routes() -> Generator[str, None, None]:
    """Yields URL routes for the server pages, since they're not linked from the main website.

    Yields:
        Generator[str, None, None]: URL routes
    """
    for filename in os.listdir(os.path.join(ROOT_DIR, "templates", "content", "servers")):
        yield "/servers/" + removesuffix(removesuffix(filename, ".html.jinja2"), ".md").replace(
            os.sep, "/"
        ) + ".html"
        # see `get_static_routes`


@freezer.register_generator
def get_redirect_page_routes() -> Generator[str, None, None]:
    """Yields URL routes for pages which exist solely to redirect. We use these similarly to a URL
    shortener, providing nicer URLs to print or distribute.

    This generator wouldn't be necessary if we used these links from our About pages, but that
    would add an unnecessary redirect in the middle when coming from those pages.

    Yields:
        Generator[str, None, None]: URL routes
    """
    yield from ["/newsletter.html", "/slack.html", "/discord.html"]


def freeze():
    """this seemingly useless method is used to provide a stable API if the freeze provider changes
    in the future

    https://pythonhosted.org/Frozen-Flask/#finding-urls
    Currently flask_frozen will implicitly find routes (in our case) if there is a url_for call to
    them. Since none of the static assets are loaded like this, and the server pages are not linked
    to at all from the main site, the two above generators provide routes for them.

    The unused get_all_routes() function can be adapted in the future if explicit route listing is
    desired.
    """

    freezer.freeze()
