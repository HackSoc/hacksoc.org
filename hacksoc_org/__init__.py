import flask
import yaml
from os import path

# flask app is constructed here
app = flask.Flask(__name__, static_folder=None, template_folder=None)
# these folders are defined in the Blueprint anyway
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.jinja_env.add_extension("jinja2.ext.do")
# adds support for the jinja "do" statement

from hacksoc_org.routes import blueprint, root_dir
app.register_blueprint(blueprint)

app.config["FREEZER_DESTINATION"] = path.join(root_dir, "build")

import hacksoc_org.filters
# importing to trigger execution; decorated functions will add themselves to the app.

with open(path.join(root_dir, "templates", "context.yaml")) as fd:
    app.jinja_env.globals.update(dict(yaml.safe_load(fd)))

from hacksoc_org.freeze import freeze
from hacksoc_org.serve import serve

@app.cli.command("freeze")
def do_freeze():
    freeze()

@app.cli.command("serve")
def static_serve():
    freeze()
    serve(path.join(root_dir, "build"))