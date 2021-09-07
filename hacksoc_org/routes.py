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

root_dir = path.join(path.dirname(__file__), path.pardir)
# dirname(__file__) is the hacksoc_org python module folder
# its parent is the git repository root, directly under which the static/, and template/ folders lie

blueprint = Blueprint(
    "routes",
    __name__,
    template_folder=None,
    static_folder=path.join(root_dir, "static"),
)

blueprint.jinja_loader = jinja2.ChoiceLoader([
    FileSystemLoader(path.join(root_dir, "templates/")),
    MarkdownNewsLoader(path.join(root_dir, "templates/"))
])

@blueprint.route("/<string:page>.html")
def render_page(page : str):
    return render_template(f"content/{page}.html.jinja2") # TODO: .jinja2

@blueprint.route("/")
def index():
    return render_page("index")

@blueprint.route("/servers/<string:page>.html")
def render_server_page(page: str):
    raise NotImplemented

@blueprint.route("/minutes.html")
def render_minutes():
    # TODO: check flask priority resolution -- does render_page need to go below this?

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
            print(e)
            print("Document will be skipped.")
            continue
    
    minutes_listing.sort(key=itemgetter('date'))

    return render_template(f"content/minutes.html.jinja2", minutes=minutes_listing)

@blueprint.route("/news/list")
def news_list():
    filename = "content/news/2021-03-22-call-for-submissions copy.html.jinja2"
    # template = blueprint.jinja_loader.get_template(
    #     current_app.jinja_env,
    #     filename
    # )

    # pp(dir(template))

    # pp(blueprint.jinja_loader.get_source(
    #     current_app.jinja_env,
    #     filename
    # ))

    # pp(get_template_attribute(filename, "title"))
    # pp(get_template_attribute(filename, "lede"))

    # src = blueprint.jinja_loader.get_source(
    #     current_app.jinja_env,
    #     filename
    # )
    # template_node = current_app.jinja_env.parse(src)
    # pp(dir(template_node))
    # pp(template_node)
    # for node in template_node.find_all(jinja2.nodes.Block):
    #     pp(node)
    #     pp(node.find(jinja2.nodes.TemplateData).data)
    
    return f"""<pre>
    title = '{get_template_attribute(filename, "title")}'

    lede = '{get_template_attribute(filename, "lede")}'
    </pre>"""

@blueprint.route("/news/test")
def news_test():
    filename = "content/news/2021-03-22-call-for-submissions copy.html.jinja2"
    return render_template(filename)

@blueprint.route("/news/<string:article>.html")
def render_news(article):
    return render_template(f"content/news/{article}.html.jinja2")