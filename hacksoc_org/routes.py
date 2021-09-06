from flask import Blueprint

blueprint = Blueprint(
    "routes",
    __name__,
    template_folder=None, #TODO:
    static_folder=None, #TODO:,
    # TODO: extra template folder for content/
)

