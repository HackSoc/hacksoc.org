from jinja2 import BaseLoader, Environment
from jinja2.exceptions import TemplateNotFound

import frontmatter

import os
from typing import Tuple, Optional, Callable


class MarkdownServerLoader(BaseLoader):

    def __init__(self, path, prefix_allow=None) -> None:
        self.prefix_allowlist = prefix_allow
        self.path = path
        super().__init__()

    def get_source(self, environment: "Environment", template: str) -> Tuple[str, Optional[str], Optional[Callable[[], bool]]]:
        if not template.startswith(self.prefix_allowlist):
            raise TemplateNotFound(template)
            
        filename = os.path.join(
            self.path,
            template.removesuffix(".html.jinja2") + ".md"
        )

        print(__name__, f"{self.path=}")
        print(__name__, f"{template=}")
        print(__name__, f"{filename=}")

        if os.path.exists(filename):
            with open(filename) as fd:
                metadata, markdown = frontmatter.parse(fd.read())
                assert isinstance(metadata, dict)
                source = """
                    {% extends "server.html.jinja2" %}
                """
                for k,v in metadata.items():
                    source += f"{{% set {k} = {repr(v)} %}}\n"

                source += (
                    """{% block body %}{% filter markdown() %}\n""" + 
                    markdown + 
                    """\n{% endfilter %}{% endblock body %}"""
                )

                return (source, filename, None)

        else:
            raise TemplateNotFound(filename)