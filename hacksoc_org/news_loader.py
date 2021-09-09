import re
from typing import Callable, Optional, Tuple
from jinja2 import BaseLoader, Environment
from jinja2.exceptions import TemplateNotFound

import frontmatter

import os

class MarkdownNewsLoader(BaseLoader):

    def __init__(self, searchpath, prefix_allow=None) -> None:
        self.prefix_allowlist = prefix_allow
        self.searchpath = searchpath
        super().__init__()

    def get_source(self, environment: Environment, template: str) -> Tuple[str, str, Optional[Callable]]:
        if not template.startswith(self.prefix_allowlist):
            raise TemplateNotFound(template)
            
        filename = os.path.join(
            self.searchpath,
            template.removesuffix(".html.jinja2") + ".md"
        )
        if os.path.exists(filename):
            with open(filename) as fd:
                metadata, content = frontmatter.parse(fd.read())
                # NB: readlines() returns a list of lines WITH \n at the end

                title = metadata['title']

            source = ("""
            {% extends "article.html.jinja2" %}
            {% block title %}""" + title + """{% endblock title %}
            {% set parts | split_lede %}{% filter markdown() %}{% raw -%}"""
          + content
          + """{% endraw %}{% endfilter %}{% endset %}
            {% block lede %}{{ parts.lede }}{% endblock lede %}
            {% block text %}{{ parts.text }}{% endblock text %}
            """)

            return (source, filename, None)
            # TODO: add 3rd tuple argument for autoreloading
        else:
            raise TemplateNotFound(template)