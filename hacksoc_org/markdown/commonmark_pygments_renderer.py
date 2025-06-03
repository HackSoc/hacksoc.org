import commonmark

from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters.html import HtmlFormatter


class PygmentsRenderer(commonmark.HtmlRenderer):
    def __init__(self, options={}) -> None:
        super().__init__(options=options)
        self.formatter = HtmlFormatter()
        self.formatter.cssclass = "codehilite"
        self.formatter.wrapcode = True

    def code_block(self, node, entering) -> None:
        attrs = self.attrs(node)

        info_words = node.info.split() if node.info else []
        if len(info_words) > 0 and len(info_words[0]) > 0:
            lexer = get_lexer_by_name(info_words[0])
        else:
            lexer = guess_lexer(node.literal)

        self.cr()
        self.lit(highlight(node.literal, lexer, self.formatter))
        self.cr()
