import flask

# flask app is constructed here

app = flask.Flask(__name__, static_folder=None, template_folder=None)
# these folders are defined in the Blueprint anyway
app.debug = True
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.jinja_env.add_extension("jinja2.ext.do")
# adds support for the jinja "do" statement

import hacksoc_org.filters
# importing to trigger execution; decorated functions will add themselves to the app.

from hacksoc_org.routes import blueprint
app.register_blueprint(blueprint)