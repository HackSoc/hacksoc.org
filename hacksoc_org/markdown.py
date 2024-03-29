"""
    Wrapper module to provide a consistent Markdown handler, regardless of the library
    implementation used.
"""

import abc
from hacksoc_org.consts import CFG_MARKDOWN_IMPL
from hacksoc_org import app


class AbstractMarkdown(abc.ABC):
    @abc.abstractmethod
    def __init__(self) -> None:
        super().__init__()

    @abc.abstractmethod
    def render_markdown(self, markdown_src: str) -> str:
        pass


class Markdown2MD(AbstractMarkdown):
    def __init__(self) -> None:
        import markdown2

        self.md = markdown2.Markdown(
            extras=[
                "fenced-code-blocks",
                "cuddled-lists",
                "tables",
                # Markdown2 has a `metadata` Extra to allow frontmatter parsing
                # this is not loaded and python-frontmatter is used instead to allow the markdown parser to
                # be changed easily if required.
            ]
        )

    def render_markdown(self, markdown_src: str) -> str:
        return self.md.convert(markdown_src)


class CmarkgfmMD(AbstractMarkdown):
    def __init__(self) -> None:
        import cmarkgfm

        self.cmarkgfm = cmarkgfm

    def render_markdown(self, markdown_src: str) -> str:
        return self.cmarkgfm.github_flavored_markdown_to_html(markdown_src)


def get_markdown_cls():
    return {"markdown2": Markdown2MD, "cmark": CmarkgfmMD}[app.config[CFG_MARKDOWN_IMPL]]


_markdowner = None


def render_markdown(markdown_src: str) -> str:
    """Renders the given markdown source into HTML

    Args:
        markdown_src (str): Markdown source

    Returns:
        str: HTML text
    """
    global _markdowner

    if _markdowner is None:
        _markdowner = get_markdown_cls()()

    return _markdowner.render_markdown(markdown_src)
