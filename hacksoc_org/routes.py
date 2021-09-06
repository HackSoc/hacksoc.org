from flask import Blueprint, render_template
from jinja2 import FileSystemLoader
from os import path

root_dir = path.join(path.dirname(__file__), path.pardir)
# dirname(__file__) is the hacksoc_org python module folder
# its parent is the git repository root, directly under which the static/, and template/ folders lie

blueprint = Blueprint(
    "routes",
    __name__,
    template_folder=path.join(root_dir, "templates/"),
    static_folder=path.join(root_dir, "static"),
)

@blueprint.route("/<string:page>.html")
def render_page(page : str):
    return render_template(f"content/{page}.html.jinja2") # TODO: .jinja2

@blueprint.route("/")
def index():
    return render_page("index")