# Adding features in Python

| **You need to know** |                       |
|----------------------|-----------------------|
| Essential:           | Python                |
| Helpful:             | Experience with Flask |

## Jinja filters and functions
Filters and functions are Python functions that are made available to Jinja templates. They're appropriate to use (instead of a Jinja macro) when you need to get extra information out of Python and into a Jinja template that's annoying or impossible to do by passing context to the template, or when you need to do extensive processing on the input that's easier to achieve in Python than with Jinja's builtin functions (eg regular expressions). A Jinja *function* is just a Jinja *filter* that takes exactly zero arguments; filters must always take at least one argument. Both of these are defined in `filters.py`. 

*Filters* have the `@app.template_filter()` decorator applied to them.  
*Functions* have the `@app.template_global()` decorator applied to them.

## Adding a new kind of page (adding URL routes)
`routes.py` defined the mappings between URL routes and templates; if the new page will be served at /pagename.html and requires no additional context to be passed to it, then you probably don't need to define a new route, `render_page` will take care of it. Otherwise, you'll need to add a new URL route that (eventually) returns the value of a `render_template` call. Consult [URL Route Registrations](https://flask.palletsprojects.com/en/2.0.x/api/#url-route-registrations) for more details about routing.

### Loading from files that aren't Jinja templates
You will notice that despite the majority of news articles being written in Markdown, the `render_news` endpoint attempts to render a template ending in `.html.jinja2`. This is achieved with some magic in the custom [MarkdownNewsLoader](../hacksoc_org/news_loader.py) (and similarly for servers). Any custom loader must extend jinja2.BaseLoader and provide a `get_source` method (see the Jinja documentation on [Loaders](https://jinja.palletsprojects.com/en/3.0.x/api/#loaders)). MarkdownNewsLoader, for instance, loads the body and frontmatter from a Markdown file and inserts them on-the-fly into some Jinja template source before returning it, as if a Jinja template really did exist with that filename and those contents.

NB: The Jinja documentation uses the term "template" to refer to any of:
 - A template *name* (the string passed to `render_template` and later to `get_source`)
 - A template itself, that can be provided context and be rendered
 - A Template node, the root of the Jinja abstract syntax tree (AST)

`routes.py` adds all the custom loaders together with a `ChoiceLoader`, which will try each loader in turn. Make sure that your custom loader only returns template sources for the intended templates. For example, if MarkdownNewsLoader did not check that Markdown files were in the `content/news/` subpath, it would accidentally find the server pages, but return them as if they were news articles, skipping all the processing that MarkdownServerLoader wants to perform on them. If a given `template` argument isn't relevant to your custom loader, just raise `TemplateNotFoundError(template)`.

## Modifying freeze 
*Freezing* (the process of rendering all possible URL routes to HTML files that can be served by nginx) is handled by `freeze.py`. For convenience, it leans heavily on `frozen-flask`. For a URL route to be frozen, it must satisfy one of the following (condensed as some of the cases in the frozen-flask documentation don't apply):
 - Be the root route (`/`)
 - Be in the [navbar](../templates/nav.html.jinja2) with a `page` link (rather than a `href` link)
 - Be linked from another rendered page via a `url_for` link (see [Creating &amp; modifying simple pages](creating_modifying_simple_pages.md))
 - Be an explicitly listed route via a URL generator

[URL generators](https://pythonhosted.org/Frozen-Flask/#url-generators) should only be used for files that aren't intended to be part of the main site, or are intended to be "unlisted". If there's no chain of links from the main page to another page, then you can't really expect anyone to find that page organically. Implementing a URL generator just requires adding a Python function that calls `yield` with each of the routes you want to ensure are rendered, and decorating the function with `@freezer.register_generator`.

## Modifying the Markdown handler
All things Markdown are hidden away in `markdown.py` so the rest of the package doesn't have to worry about it. It exports a single function, `render_markdown` which takes a Markdown source string and returns a rendered HTML string. Even if this wraps a single function from a Markdown library, if that library ever changes in the future it means that the codebase only needs to be changed in one place. 

Currently the website uses [`python-markdown2`][pymd2] and loads the following extras:
 - `fenced-code-blocks` allow blocks of code to be placed between triple-backticks (\`\`\`)
 - `cuddled-lists` remove the requirement of a blank line between a paragraph and a list
 - `tables` add GFM-style tables

Since the server READMEs use fenced code blocks and AGMs will often use many tables, any replacment library must support at least these. 

### Choice of Markdown libraries
Choosing a Markdown backend is not straightforward; implementations vary in their interpretation of the spec (Gruber's `markdown.pl` or the less ambiguous CommonMark standard) and their extra features (tables, code block highlighting, smart quotes). Currently [`markdown2`][pymd2] is used, although its non-conformance with CommonMark makes a replacement desireable.

To help test between Markdown backends, non-default backends can be selected with the `--markdown` command-line option. Only [`cmark`](https://github.com/commonmark/cmark) is available (provided through the [`cmarkgfm`](https://github.com/theacodes/cmarkgfm) Python bindings).

```
# Equivalent; markdown2 is the default backend
hacksoc_org run
hacksoc_org run --markdown markdown2

# Use cmark instead
hacksoc_org run --markdown cmark

# this works with all subcommands
hacksoc_org freeze --markdown cmark
```


## Serving Flask in production
Some of Flask's extra power (handling POST requests, HTTP redirects) require it to be run in production (as opposed to generating HTML files and serving those from a static web server). Currently the [configuration](../.flaskenv) of Flask puts it into debug mode. This is extremely unsafe to run in production. Secondly, `hacksoc_org run` or `app.run()` should not be used in production as it used Flask's built-in development server, which is not suitable for production use even when debug mode is disabled. Instead, consult [Flask's documentation](https://flask.palletsprojects.com/en/2.0.x/deploying/#self-hosted-options) on options for WSGI and CGI servers.


[pymd2]: https://github.com/trentm/python-markdown2/wiki