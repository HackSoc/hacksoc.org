# Creating &amp; modifying simple pages

| **You should know** |                                   |
|---------------------|-----------------------------------|
| Essential:          | Basic HTML or Markdown formatting |
| Helpful:            | CSS                               |

In this context, *simple* pages are ones where the content is mostly HTML and require little or no use of Jinja features beyond the essentials. All HTML pages are stored in `templates/content/` and named `pagename.html.jinja2`. This will produce a page at `hacksoc.org/pagename.html`. 

All pages must include three things:
 - `{% extends "base.html.jinja2" %}`
 - `title` block &ndash; this is put into the `<title>` element in `<head>`.
   - This title will be followed by `| HackSoc - the computer science society`, so you don't need to mention "HackSoc" in your title.
   - **Avoid:** `HackSoc events`, `Society events`
   - **Prefer:** `Our events`, `events`
 - `body` block &ndash; this contains the content of the page, and is put inside the main container.

As with news articles, long sections of pages can be written using the `markdown()` filter. Remember that whether in Markdown or HTML, Headings 1 and 2 are already used, so headings within `{% block body%}` should start at Heading 3.

## HTML formatting
You should know *what* HTML tags are, this list gives some rules of thumb on how they are used in this website:
 - Any amount of text a sentence or longer should be inside a `<p>` (paragraph) tag.
 - Avoid `<br>`:
   - Use multiple `<p>` tags for paragraph breaks in text
   - Use CSS `margin` and `padding` for spacing between elements.
   - Use `<pre>` for blocks that need whitespace (newlines and indentations) preserved
     - You can also use [`white-space`](https://developer.mozilla.org/en-US/docs/Web/CSS/white-space) set to `pre-line` to respect newlines only (ignoring other whitespace as with normal HTML).
 - Use `<strong>` and `<em>` (emphasis) instead of `<b>` (bold) and `<i>` (italic) inside paragraphs.
 - Consider using `<span class="descriptive-name">` instead of `<strong>`/`<em>` for other kinds of text (outside of paragraphs); use or create a CSS class that describes the *purpose* of that element (warning, date, subtitle) instead of the formatting. This means that it's easy to change the formatting later, but keep the original intention of the markup.

## Additional styles
The site-wide stylesheet will be sufficient for most pages, but if you find yourself needing to add CSS, using the `style` attribute on a HTML element is highly discouraged. Instead add a page-specific stylesheet with the `stylesheets` block.

```html
{% extends "base.html.jinja2" %}

{% block title %} My page name {% endblock title %}

{% block stylesheets %}
<style>
    .tabular {
        font-variant-numeric: tabular-nums;
        font-weight: bolder;
    }
</style>
{% endblock stylesheets %}

{% block body %}
<p>You can contact us on <span class="tabular">0909 8790102</span></p>
{% endblock body %}
```

## Modifying the site template
See [Creating &amp; modifying complex pages](creating_modifying_complex_pages.md).

## A new page doesn't appear when building the website!
`frozen-flask` only generates pages which have a `url_for` link pointing to them. Usually pages on the website should have a link from `index.html`, or from another page which is linked from `index.html` (and so on,). If a new page is being written, it's possible that such a link doesn't yet exist. This only happens when running `hacksoc_org build` or `hacksoc_org serve`, as `hacksoc_org run` will find any page, even if it's not been linked to. Make sure to test with `build` or `serve`.

### Adding a link to the navbar
The navbar is constructed in [`templates/nav.html.jinja2`](../templates/nav.html.jinja2). The first block, titled `{% set nav|from_yaml %}` contains the items of the navbar:
 - `text`: the visible text of the link (eg. My Page name)
 - `page` or `href`:
   - **Internal** links should use `page` to give the name of the page *without the `.html` extension*; eg `page: mypage` for a file named `templates/content/mypage.html`. This will automatically generate a `url_for` link, so any internal page on the navbar will be generated.
   - **External** links should use `href`, which is put directly into the `href` field of the `<a>` tag.

### Adding a link inside a page
If the new page is unworthy of a place on the sacred navigation bar, then it must be linked to from another page (otherwise, how will visitors find it?). Inside the link tag, instead of a normal URL in the `href` attribute, pass `{{ url_for('.render_page', page='mypage') }}`. This will automatically update the URL if the structure of the site changes, and will ensure the new page is generated. 

This **should** also work in Markdown (not verified yet) (excluding `.md` news pages):
```markdown
Connect with us on [IRC!]({{ url_for('.render_page', page='irc') }})

Make sure to read the [Code of Conduct][CoC] first though.

[CoC]: {{url_for('.render_page', page='coc')}}
```


## Examples
Pages that count as "simple" currently include:
 - [about.html](../templates/content/about.html.jinja2)
 - [coc.html](../templates/content/coc.html.jinja2)
 - [irc.html](../templates/content/irc.html.jinja2)