import re
from typing import Callable, Optional, Tuple
from jinja2 import BaseLoader, Environment
from jinja2.exceptions import TemplateNotFound

import frontmatter

import os

from hacksoc_org.util import removesuffix


class MarkdownNewsLoader(BaseLoader):
    def __init__(self, searchpath: str, prefix_allow: Optional[str] = None) -> None:
        """
        Args:
            searchpath ([str]): base directory that `template` is relative to
            prefix_allow ([str], optional): if provided, only allow `template`s matching the
            provided prefix
        """
        self.prefix_allowlist = prefix_allow
        self.searchpath = searchpath
        super().__init__()

    def get_source(
        self, environment: Environment, template: str
    ) -> Tuple[str, str, Optional[Callable[[], bool]]]:
        """Superclass override (https://jinja.palletsprojects.com/en/3.0.x/api/#loaders)

        When told to find a template with name `foo.html.jinja2`, will attempt to find a template
        with name `foo.md` and wrangle it into Jinja format.

        Raises:
            TemplateNotFound: [description]

        Returns:
            Tuple[str,str,Optional[Callable[[],bool]]]: (source, filename, is_uptodate);
                `source` is the Jinja template source,
                `filename` is the path to the file that Jinja can use for stack
                traces,
                `is_uptodate` (if provided) is used for template reloading; if
                it returns `False` then the template is reloaded.
        """

        if not template.startswith(self.prefix_allowlist):
            raise TemplateNotFound(template)

        filename = os.path.join(self.searchpath, removesuffix(template, ".html.jinja2") + ".md")
        if os.path.exists(filename):
            with open(filename) as fd:
                metadata, content = frontmatter.parse(fd.read())
                # NB: readlines() returns a list of lines WITH \n at the end

                title = metadata["title"]

            source = (
                """
            {% extends "article.html.jinja2" %}
            {% block title %}"""
                + title
                + """{% endblock title %}
            {% set parts | split_lede %}{% filter markdown() %}{% raw -%}"""
                + content
                + """{% endraw %}{% endfilter %}{% endset %}
            {% block lede %}{{ parts.lede }}{% endblock lede %}
            {% block text %}{{ parts.text }}{% endblock text %}
            """
            )

            return (source, filename, None)
            # TODO: add 3rd tuple argument for autoreloading
        else:
            raise TemplateNotFound(template)
