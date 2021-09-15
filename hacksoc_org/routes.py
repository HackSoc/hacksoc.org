"""
    Defines Flask URL route handlers. Exports `blueprint` to be mounted by app
    onto the root.
"""

from hacksoc_org.server_loader import MarkdownServerLoader
from flask import Blueprint, render_template, url_for, current_app, get_template_attribute
from jinja2 import FileSystemLoader

from hacksoc_org.news_loader import MarkdownNewsLoader

import os
from os import path
import re
from datetime import date
from operator import itemgetter
from pprint import pprint as pp

import jinja2

root_dir = path.abspath(path.join(path.dirname(__file__), path.pardir))
template_dir = path.join(root_dir, "templates")
# dirname(__file__) is the hacksoc_org python module folder
# its parent is the git repository root, directly under which the static/, and template/ folders lie

blueprint = Blueprint(
    "routes",
    __name__,
    template_folder=None,
    static_folder=path.join(root_dir, "static"),
    static_url_path='/static'
)

blueprint.jinja_loader = jinja2.ChoiceLoader([
    FileSystemLoader(template_dir),
    MarkdownNewsLoader(template_dir, prefix_allow=os.path.join("content", "news")),
    MarkdownServerLoader(template_dir, prefix_allow=os.path.join("content", "servers"))
])

@blueprint.route("/<string:page>.html")
def render_page(page : str):
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
    return render_template(f"content/servers/{page}.html.jinja2")

@blueprint.route("/minutes.html")
def render_minutes():
    """Special case for minutes.html, which enumerates minutes documents and provides as context

    Returns:
        str: Full HTML page
    """

    # this could be put into a get_minutes() function in filters.py, similar to 
    # get_news. This function could be removed and minutes.html handled by 
    # render_page

    re_filename = re.compile(r"^(\d{4}-[01]\d-[0123]\d)-(.*)\.pdf$")

    minutes_listing = []
    for filename in os.listdir(path.join(root_dir, "static", "minutes")):
        match = re_filename.match(filename)
        if match is None: continue

        try:
            minutes_listing.append({
                'date': date.fromisoformat(match[1]),
                'meeting': match[2],
                'url': url_for('.static', filename=f"minutes/{filename}")
            })
        except ValueError as e:
            print(f"Error while parsing {filename}:")
            print("", e)
            print(" Document will be skipped.")
            continue
    
    minutes_listing.sort(key=itemgetter('date'))

    return render_template(f"content/minutes.html.jinja2", minutes=minutes_listing)

@blueprint.route("/news/<string:article>.html")
def render_news(article: str):
    """Renders a news article, providing the template with the publishing date

    Args:
        article (str): article basename (no extension or path)

    Returns:
        str: Full HTML page
    """
    return render_template(f"content/news/{article}.html.jinja2", date=date.fromisoformat(article[:10]))