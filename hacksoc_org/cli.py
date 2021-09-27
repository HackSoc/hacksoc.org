import click

from hacksoc_org import app, ROOT_DIR
from hacksoc_org.consts import *

from os import path


@click.group()
@click.option(
    "--markdown",
    type=click.Choice(["markdown2", "cmark"], case_sensitive=False),
    default="markdown2",
)
def main(markdown: str):
    # this gets executed before every valid command; prime opportunity to do config
    print("=" * 8, "main()", "=" * 8)
    app.config[CFG_MARKDOWN_IMPL] = markdown
    print(f"Using markdown implementation '{markdown}'")


@main.command()
def run():
    app.run()


from hacksoc_org.freeze import freeze
from hacksoc_org.serve import serve


@main.command("freeze")
def do_freeze():
    """Called on `flask freeze`. Renders the site to HTML in the build/ directory"""
    freeze()


@main.command("serve")
def do_serve():
    """Called on `flask serve`. Freezes the site and starts a local server. Should be
    near-indistinguishable from `flask run`."""
    freeze()
    print()
    serve(path.join(ROOT_DIR, "build"))


@main.command()
def foo():
    print("Bar")
