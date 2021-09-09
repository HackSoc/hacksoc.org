# Writing articles

| **You should know** |                                                          |
|---------------------|----------------------------------------------------------|
| Essential:          |                                                          |
| Helpful:            | Markdown formatting (explained here *briefly* otherwise) |

## Using Markdown
For simple articles that just need basic formatting, lists, and tables, writing articles in Markdown is straightforward. 

### File naming
Articles should be named `YYYY-MM-DD-article-title.md`; the full year, zero-padded month and day (2nd January 1999 is written as 2021-01-02). The `article-title` section should be representative of the article as it will be visible in URLs. Files are placed in `templates/content/news`.

### Frontmatter
In the markdown files, metadata about the article is given in the *frontmatter* section. This is delimited between `---` at the start of the file. Currently, the only metadata attribute is `title`, which should be the plain-text title of the article. Since the title appears here, you **do not need to include the title in the body of the article**.

### Headings
Since the title of the website (HackSoc.org) is Heading 1, the title of the article is Heading 2, headings within the article should start from Heading 3 (`### Heading`).

### Formatting
Standard markdown formatting applies:
-  Surround with `*` or `_` for italics 
- `**` or `__` for bold. 
- Bullet Lists start with a space, a hyphen, then another space before the items
- Numbered lists start with a space, a number, a full stop, and then a space before the items
- Nested list items must be indented 4 extra spaces per level.
- Hyperlinks are given as the link text in square brackets, followed by an immediate hyperlink in round brackets, or a link label in square brackets

### Tables
You can use tables in the same way as in GFM (GitHub Flavoured Markdown), see the [GFM docs][GFMtables]. When writing articles for the site, please prettify the tables (ie, make sure the columns line up). It has no effect on the website but makes the source more pleasant for others to read.

### Line length
As per the [style guide][README], lines in news articles should be no longer than 80 characters. This excludes hyperlinks for practical reasons.


### Example 
```markdown
---
title: An example article
---

The first paragraph of the article is interpreted as the [lede][wikilede]. Don't
make this too long, as it will appear in the newslist on the website as well as
in social media previews.

Some text can be **bold**, and some can be *italic*. Sometimes it's useful to 
use _underscores_ __instead__ for the same effect. 
 - Lists don't need a blank line between them and a paragraph
    - Nested list items should be indented at least 4 spaces more
        - Like this

If [hyperlinks](https://en.wikipedia.org/wiki/Hyperlink) are short, they can be
given in the text. Otherwise, or if the same link is repeated, use 
[link labels][GFMlinklabels] and provide the URL at the bottom of the article.

|                                  |                                   |
|----------------------------------|-----------------------------------|
| Tables need a "heading" column   | even if it's not used             |
| You may find [this tool][mdtabs] | useful when using Markdown tables |

[wikilede]: https://en.wikipedia.org/wiki/Lead_paragraph "Lead paragraph - Wikipedia"
[GFMlinklabels]: https://github.github.com/gfm/#link-label "Link label: GitHub Flavoured Markdown Spec"
[mdtabs]: https://www.tablesgenerator.com/markdown_tables "Markdown Tables generator - TablesGenerator.com"
```

## Using HTML & Jinja
More complex articles can be written directly in HTML. These articles can also leverage the Jinja templating system. You can use any HTML elements that are appropriate.

### File naming
The same rules apply, except that the file should end in `.html.jinja2` rather than `.md`

### Templating
Any Jinja article should include these four things:
 - `{% extends "article.html.jinja2" %}`
 - `title` block with the article title
 - `lede` block with the first sentence or paragraph of the article
 - `body` block with the rest of the article

### Markdown in Jinja
If the majority of the article can be written in Markdown, but you still want the control of a Jinja article for one section, you can use the `markdown` filter. Simply surround the Markdown section with `{% filter markdown() %}` and `{% endfilter %}`, and write Markdown as above between the two tags.

 - `{% block title %} Your article Title here {% endblock title %}`
 - `{% block lede %} The first sentence or paragraph of the article here. This will be visible on the newslist as well as social media embeds {% endblock lede %}`
 - `{% block body %} {% endblock body%}`

### Example

```html
{% extends "article.html.jinja2" %}

{% block title %} An example article {% endblock title %}

{% block lede %}
    The first paragraph of the article is interpreted as the 
    <a href="https://en.wikipedia.org/wiki/Lead_paragraph">lede</a>. Don't make 
    this too long, as it will appear in the newslist on the website as well as
    in social media previews.
{% endblock lede %}

{% block body %}
    <p>
        The body is normal HTML unless you specify otherwise; make sure to use 
        <code>&lt;p&gt;</code> tags for paragraphs so that the styling remains
        consistent.
    </p>

{% filter markdown() %}
### Some markdown tips
Although HackSoc prefers the "fenced" code block style, Markdown also supports
code blocks simply by indenting them 4 spaces. That means that if you indent the
markdown filter 4 (or more) spaces, it will put the whole input in a &lt;pre&gt;
block. So remember to start markdown input with no indentation whatsoever.
{% endfilter %}

{% endblock body %}
```

[GFMtables]: https://github.github.com/gfm/#tables-extension- "Tables (extension): GitHub Flavoured Markdown Spec"
[README]: ../README.md