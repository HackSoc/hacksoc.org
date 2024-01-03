from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters.html import HtmlFormatter


class PygmentsHighlighter:
    def __init__(self) -> None:
        self.formatter = HtmlFormatter()
        self.formatter.cssclass = "codehilite"
        self.formatter.wrapcode = True

    def __call__(self, content, lang, attrs):
        if lang is None or len(lang) == 0:
            lexer = guess_lexer(content)
        else:
            lexer = get_lexer_by_name(lang)

        return highlight(content, lexer, self.formatter)
