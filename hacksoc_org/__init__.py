"""
    hacksoc_org: build system for the hacksoc.org website.

    This module contains the Flask and Jinja boilerplate, HackSoc-specific customisations for pages,
    and user convenience functionality for local testing.
"""
import sys

if sys.version_info < (3, 7):
    print(
        "Warning: you are using an older version of Python ("
        + str(sys.version)
        + ") that is not supported by HackSoc.org."
    )


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

# Use existing config if it is present, otherwise assume production location,
# this only applies to freezing and doesn't affect the base URL for debugging.
app.config.setdefault("FREEZER_BASE_URL", "https://www.hacksoc.org")

import hacksoc_org.filters

# importing to trigger execution; decorated functions will add themselves to the app.

# random global values are put in context.yaml and will be available to all templates
with open(path.join(ROOT_DIR, "templates", "context.yaml"), encoding="utf-8") as fd:
    app.jinja_env.globals.update(dict(yaml.safe_load(fd)))
