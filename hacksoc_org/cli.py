from typing import Callable, Dict
from hacksoc_org import app
from hacksoc_org.consts import *
from hacksoc_org.freeze import freeze
from hacksoc_org.serve import serve

import argparse

subcommand_handlers: Dict[str, Callable] = {}


def subcommand(command_str: str) -> Callable[[Callable], Callable]:
    def inner(fn):
        subcommand_handlers[command_str] = fn
        return fn

    return inner


def main(args=None):
    parser = argparse.ArgumentParser(
        allow_abbrev=False,
        epilog="""
SUBCOMMANDS

  run
    Starts a local development server on https://localhost:5000/. Automatically
    reloads when templates or Python code is changed. Recommended while 
    developing pages or features.

  freeze
    Saves all URL routes to HTML files and copies `static/` to the `build/` 
    directory. The resulting directory can be used with any standard HTTP
    server (nginx, Apache, etc). In development, recommend using `serve` 
    instead for convenience.

  serve
    Calls `freeze` then starts a local HTTP server from `build/` on 
    https://localhost:5000/. Will not automatically rebuild the website on
    content change, you will need to re-run `serve`. Recommended to use this at
    least once to check that a) new content is part of the "frozen" site and b)
    no errors occur in freezing the site.
""".strip(),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "action", choices=subcommand_handlers.keys(), help="Subcommand to run (see below)"
    )

    parser.add_argument(
        "--markdown",
        choices=[
            "markdown2",
            "cmark",
            "commonmark",
            "mistletoe",
            "markdown-it",
        ],
        default="markdown2",
        help="Markdown backend to use (default markdown2)",
    )

    args = parser.parse_args(args=args)

    app.config[CFG_MARKDOWN_IMPL] = args.markdown

    subcommand_handlers[args.action]()


@subcommand("run")
def do_run():
    app.run()


@subcommand("freeze")
def do_freeze():
    freeze()


@subcommand("serve")
def do_serve():
    freeze()
    print()
    serve()


if __name__ == "__main__":
    main()
