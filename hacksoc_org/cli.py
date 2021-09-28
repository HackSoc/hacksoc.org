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
    parser = argparse.ArgumentParser(allow_abbrev=False)

    parser.add_argument("action", choices=subcommand_handlers.keys())
    # TODO: add help to prelude/preamble

    parser.add_argument("--markdown", choices=["markdown2", "cmark"], default="markdown2")

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
