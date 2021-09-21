"""
    hacksoc_org: build system for the hacksoc.org website.

    This module contains the Flask and Jinja boilerplate, HackSoc-specific customisations for pages,
    and user convenience functionality for local testing.
"""


import flask
import yaml
from os import path

# flask app is constructed here
app = flask.Flask(__name__, static_folder=None, template_folder=None)
# these folders are defined in the Blueprint anyway
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.jinja_env.add_extension("jinja2.ext.do")
# adds support for the jinja "do" statement

from hacksoc_org.routes import blueprint, ROOT_DIR

app.register_blueprint(blueprint)

app.config["FREEZER_DESTINATION"] = path.join(ROOT_DIR, "build")

import hacksoc_org.filters

# importing to trigger execution; decorated functions will add themselves to the app.

# random global values are put in context.yaml and will be available to all templates
with open(path.join(ROOT_DIR, "templates", "context.yaml")) as fd:
    app.jinja_env.globals.update(dict(yaml.safe_load(fd)))

from hacksoc_org.freeze import freeze
from hacksoc_org.serve import serve


@app.cli.command("freeze")
def do_freeze():
    """Called on `flask freeze`. Renders the site to HTML in the build/ directory"""
    freeze()


@app.cli.command("serve")
def static_serve():
    """Called on `flask serve`. Freezes the site and starts a local server. Should be
    near-indistinguishable from `flask run`."""
    freeze()
    print()
    serve(path.join(ROOT_DIR, "build"))
