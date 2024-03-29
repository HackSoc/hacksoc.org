"""
    Defines Flask URL route handlers. Exports `blueprint` to be mounted by app onto the root.
"""

from hacksoc_org.loaders import MarkdownServerLoader, MarkdownNewsLoader
from flask import Blueprint, Response, render_template, url_for
from jinja2 import FileSystemLoader

import os
from os import path
import re
from datetime import date, datetime, timezone
from operator import attrgetter, itemgetter

import jinja2

ROOT_DIR = path.abspath(path.join(path.dirname(__file__), path.pardir))
TEMPLATE_DIR = path.join(ROOT_DIR, "templates")
# dirname(__file__) is the hacksoc_org python module folder
# its parent is the git repository root, directly under which the static/, and template/ folders lie

blueprint = Blueprint(
    "routes",
    __name__,
    template_folder=None,
    static_folder=path.join(ROOT_DIR, "static"),
    static_url_path="/static",
)

blueprint.jinja_loader = jinja2.ChoiceLoader(
    [
        FileSystemLoader(TEMPLATE_DIR),
        MarkdownNewsLoader(TEMPLATE_DIR, prefix_allow=os.path.join("content", "news")),
        MarkdownServerLoader(TEMPLATE_DIR, prefix_allow=os.path.join("content", "servers")),
    ]
)


@blueprint.route("/<string:page>.html")
def render_page(page: str):
    """Renders a simple page, with no additional context passed.

    Serves `content/foo.html.jinja2` at `/foo.html`

    Args:
        page (str): name of the page (with no extension)

    Returns:
        str: Full HTML page
    """
    return render_template(f"content/{page}.html.jinja2")


@blueprint.route("/")
def index():
    """Handles / serving index.html

    Returns:
        str: Full HTML page
    """
    return render_page("index")


@blueprint.route("/servers/<string:page>.html")
def render_server_page(page: str):
    """Handles server READMEs (not part of main website but copied off by each server)

    Args:
        page (str): server hostname (eg runciman)

    Returns:
        str: Full HTML page
    """
    return render_template(f"content/servers/{page}.html.jinja2")


@blueprint.route("/minutes.html")
def render_minutes():
    """Special case for minutes.html, which enumerates minutes documents and provides as context

    Returns:
        str: Full HTML page
    """

    # this could be put into a get_minutes() function in filters.py, similar to get_news. This
    # function could be removed and minutes.html handled by render_page

    re_filename = re.compile(r"^(\d{4}-[01]\d-[0123]\d)_(.*)\.pdf$")

    MINUTES_DIR = path.join(ROOT_DIR, "static", "minutes")

    committees = sorted(
        list(filter(lambda de: de.is_dir(), os.scandir(MINUTES_DIR))),
        key=attrgetter("name"),
        reverse=True,
    )

    assert len(committees) > 0, "No committee folders detected in /static/minutes!"

    minutes_listing = {}
    for committee_dir in committees:
        minutes_listing[committee_dir.name] = []

        for filename in os.listdir(path.join(MINUTES_DIR, committee_dir.name)):
            match = re_filename.match(filename)
            if match is None:
                continue

            try:
                minutes_listing[committee_dir.name].append(
                    {
                        "date": date.fromisoformat(match[1]),
                        "meeting": match[2].replace("_", " "),
                        "url": url_for(
                            ".static", filename=f"minutes/{committee_dir.name}/{filename}"
                        ),
                    }
                )
            except ValueError as e:
                print(f"Error while parsing {filename}:")
                print("", e)
                print(" Document will be skipped.")
                continue

            minutes_listing[committee_dir.name].sort(key=itemgetter("date"), reverse=True)

    return render_template("content/minutes.html.jinja2", listing=minutes_listing)


@blueprint.route("/news/<string:article>.html")
def render_news(article: str):
    """Renders a news article, providing the template with the publishing date

    Args:
        article (str): article basename (no extension or path)

    Returns:
        str: Full HTML page
    """
    return render_template(
        f"content/news/{article}.html.jinja2", date=date.fromisoformat(article[:10])
    )


@blueprint.route("/rss.xml")
def render_rss_feed():
    """Render the rss feed using template.

    Returns:
        str: RSS XML document
    """
    return Response(
        render_template("content/rss.xml.jinja2", generate_datetime=datetime.now(timezone.utc)),
        content_type="application/xml",
    )


@blueprint.route("/atom.xml")
def render_atom_feed():
    """Render the atom feed using template.

    Returns:
        str: Atom XML document
    """
    return Response(
        render_template("content/atom.xml.jinja2", generate_datetime=datetime.now(timezone.utc)),
        content_type="application/xml",
    )
