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
        self.options = cmarkgfm.Options.CMARK_OPT_UNSAFE

    def render_markdown(self, markdown_src: str) -> str:
        return self.cmarkgfm.github_flavored_markdown_to_html(markdown_src, self.options)


class CommonMarkMD(AbstractMarkdown):
    def __init__(self) -> None:
        import commonmark
        from .commonmark_pygments_renderer import PygmentsRenderer

        self.parser = commonmark.Parser()
        self.renderer = PygmentsRenderer()

    def render_markdown(self, markdown_src: str) -> str:
        ast = self.parser.parse(markdown_src)
        return self.renderer.render(ast)


class MistletoeMD(AbstractMarkdown):
    def __init__(self) -> None:
        import mistletoe
        from .mistletoe_pygments_renderer import PygmentsRenderer

        self.renderer = PygmentsRenderer()
        self.Document = mistletoe.Document

    def render_markdown(self, markdown_src: str) -> str:
        return self.renderer.render(self.Document(markdown_src))


class MarkdownItMD(AbstractMarkdown):
    def __init__(self) -> None:
        import markdown_it
        from .markdownit_pygments_highlighter import PygmentsHighlighter

        self.md = markdown_it.MarkdownIt().enable("table")
        self.md.options["highlight"] = PygmentsHighlighter()

    def render_markdown(self, markdown_src: str) -> str:
        return self.md.render(markdown_src)


def get_markdown_cls():
    return {
        "markdown2": Markdown2MD,
        "cmark": CmarkgfmMD,
        "commonmark": CommonMarkMD,
        "mistletoe": MistletoeMD,
        "markdown-it": MarkdownItMD,
    }[app.config[CFG_MARKDOWN_IMPL]]


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
