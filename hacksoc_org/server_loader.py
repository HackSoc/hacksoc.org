from jinja2 import BaseLoader, Environment
from jinja2.exceptions import TemplateNotFound

import frontmatter

import os
from typing import Tuple, Optional, Callable

from hacksoc_org.util import removesuffix


class MarkdownServerLoader(BaseLoader):
    def __init__(self, path: str, prefix_allow: Optional[str] = None) -> None:
        """
        Args:
            searchpath ([str]): base directory that `template` is relative to
            prefix_allow ([str], optional): if provided, only allow `template`s matching the
            provided prefix
        """
        self.prefix_allowlist = prefix_allow
        self.path = path
        super().__init__()

    def get_source(
        self, environment: "Environment", template: str
    ) -> Tuple[str, Optional[str], Optional[Callable[[], bool]]]:
        """Superclass override (https://jinja.palletsprojects.com/en/3.0.x/api/#loaders)

        When told to find a template with name `foo.html.jinja2`, will attempt to find a template
        with name `foo.md` and wrangle it into Jinja format.

        Raises:
            TemplateNotFound: [description]

        Returns:
            Tuple[str,str,Optional[Callable[[],bool]]]: (source, filename, is_uptodate);
                `source` is the Jinja template source,
                `filename` is the path to the file that Jinja can use for stack traces,
                `is_uptodate` (if provided) is used for template reloading; if it returns `False`
                then the template is reloaded.
        """
        if not template.startswith(self.prefix_allowlist):
            raise TemplateNotFound(template)

        filename = os.path.join(self.path, removesuffix(template, ".html.jinja2") + ".md")

        if os.path.exists(filename):
            with open(filename) as fd:
                metadata, markdown = frontmatter.parse(fd.read())
                assert isinstance(metadata, dict)
                source = """
                    {% extends "server.html.jinja2" %}
                """
                for k, v in metadata.items():
                    source += f"{{% set {k} = {repr(v)} %}}\n"

                source += (
                    """{% block body %}{% filter markdown() %}\n"""
                    + markdown
                    + """\n{% endfilter %}{% endblock body %}"""
                )

                return (source, filename, None)

        else:
            raise TemplateNotFound(filename)
