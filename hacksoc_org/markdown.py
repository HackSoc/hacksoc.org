"""
    Wrapper module to provide a consistent Markdown handler, regardless of the
    library implementation used.
"""

import markdown2

markdowner = markdown2.Markdown(extras=[
    'fenced-code-blocks',
    'cuddled-lists',
    'tables',
    # Markdown2 has a `metadata` Extra to allow frontmatter parsing
    # this is not loaded and python-frontmatter is used instead
    # to allow the markdown parser to be changed easily if required.
])

def render_markdown(markdown_src : str) -> str:
    """Renders the given markdown source into HTML

    Args:
        markdown_src (str): Markdown source

    Returns:
        str: HTML text
    """
    return markdowner.convert(markdown_src)