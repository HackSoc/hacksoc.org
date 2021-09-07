import re
from typing import Callable, Optional, Tuple
from jinja2 import BaseLoader, Environment
from jinja2.exceptions import TemplateNotFound

import frontmatter

import os
from pprint import pp

class MarkdownNewsLoader(BaseLoader):

    def __init__(self, path) -> None:
        self.path = path
        print(__name__, f"{path=}")
        super().__init__()

    def get_source(self, environment: Environment, template: str) -> Tuple[str, str, Optional[Callable]]:
        print(f"{template=}")
        filename = os.path.join(
            self.path,
            template.removesuffix(".html.jinja2") + ".md"
        )
        if os.path.exists(filename):
            with open(filename) as fd:
                metadata, content = frontmatter.parse(fd.read())
                # NB: readlines() returns a list of lines WITH \n at the end
                # TODO: frontematter parse here
                title = metadata['title']
                lede = "Lede!"


            source = """{% extends "article.html.jinja2" %}
            {% block title %}""" + title + """{% endblock title %}

            {% filter markdown() %}
            {% block lede %}""" + lede + """{% endblock lede %}
            {% block text %}
            """ + content + """
            {% endblock text %}
            {% endfilter %}
            """
            pp(source)
            
            return (source, filename, None)
            # TODO: add 3rd tuple argument for autoreloading
        else:
            raise TemplateNotFound()

lede_re = re.compile(r"(P=<lede>.*\w.*)(?:\r?\n){2,}(P=<body>.*)")
def split_lede(markdown_src : str) -> Tuple[str,str]:
    pass