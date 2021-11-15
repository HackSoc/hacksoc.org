"""
    Wrapper module to provide a consistent Markdown handler, regardless of the library
    implementation used.
"""

import abc
from hacksoc_org.consts import CFG_MARKDOWN_IMPL
from hacksoc_org import app
import textwrap
from inspect import cleandoc


class AbstractMarkdown(abc.ABC):
    @abc.abstractmethod
    def __init__(self) -> None:
        super().__init__()

    @abc.abstractmethod
    def render_markdown(self, markdown_src: str) -> str:
        pass

    @abc.abstractstaticmethod
    def key() -> str:
        pass


class Markdown2MD(AbstractMarkdown):
    """
    Default
    Not CommonMark compliant (aims to match Markdown.pl)
    """

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

    def key():
        return "markdown2"


class CmarkgfmMD(AbstractMarkdown):
    """
    CommonMark compliant
    Doesn't support syntax highlighting
    """

    def __init__(self) -> None:
        import cmarkgfm

        self.cmarkgfm = cmarkgfm
        self.options = cmarkgfm.Options.CMARK_OPT_UNSAFE

    def render_markdown(self, markdown_src: str) -> str:
        return self.cmarkgfm.github_flavored_markdown_to_html(markdown_src, self.options)

    def key() -> str:
        return "cmark"


class CommonMarkMD(AbstractMarkdown):
    """
    CommonMark compliant
    Doesn't support tables
    """

    def __init__(self) -> None:
        import commonmark
        from .commonmark_pygments_renderer import PygmentsRenderer

        self.parser = commonmark.Parser()
        self.renderer = PygmentsRenderer()

    def render_markdown(self, markdown_src: str) -> str:
        ast = self.parser.parse(markdown_src)
        return self.renderer.render(ast)

    def key() -> str:
        return "commonmark"


class MistletoeMD(AbstractMarkdown):
    """
    CommonMark compliant
    """

    def __init__(self) -> None:
        import mistletoe
        from .mistletoe_pygments_renderer import PygmentsRenderer

        self.renderer = PygmentsRenderer()
        self.Document = mistletoe.Document

    def render_markdown(self, markdown_src: str) -> str:
        return self.renderer.render(self.Document(markdown_src))

    def key() -> str:
        return "mistletoe"


class MarkdownItMD(AbstractMarkdown):
    """
    CommonMark compliant
    """

    def __init__(self) -> None:
        import markdown_it
        from .markdownit_pygments_highlighter import PygmentsHighlighter

        self.md = markdown_it.MarkdownIt().enable("table")
        self.md.options["highlight"] = PygmentsHighlighter()

    def render_markdown(self, markdown_src: str) -> str:
        return self.md.render(markdown_src)

    def key() -> str:
        return "markdown-it"


implementations = {
    c.key(): c
    for c in [
        Markdown2MD,
        CmarkgfmMD,
        CommonMarkMD,
        MistletoeMD,
        MarkdownItMD,
    ]
}


def get_markdown_cls():
    return implementations[app.config[CFG_MARKDOWN_IMPL]]


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


def get_backend_help() -> str:
    s = "MARKDOWN BACKENDS\n\n"

    for impl in implementations.values():
        s += "  " + impl.key() + "\n"
        if impl.__doc__ is not None:
            s += textwrap.indent(cleandoc(impl.__doc__), "    ")
        s += "\n\n"
    return s.strip()
