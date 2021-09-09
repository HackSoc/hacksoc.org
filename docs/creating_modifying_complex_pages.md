# Creating &amp; modifying complex pages

| **You should know** |                                       |
|---------------------|---------------------------------------|
| Essential:          | HTML, basic [Jinja syntax][jinjadocs] |
| Helpful:            | CSS, JS                               |

Complex pages don't really follow a pattern like simple pages and news articles. Instead, here's an introduction to some of the concepts you'll find useful when writing such pages. Examples of complex pages include:
 - [`index.html.jinja2`](../templates/content/index.html.jinja2)
 - [`news.html.jinja2`](../templates/content/news.html.jinja2)
   - Most of the complexity is in `newslist.html.jinja2`, which this imports.
 - [`minutes.html.jinja2`](../templates/content/minutes.html.jinja2)

## Extending, including, importing
This topic is covered in the [Jinja documentation][jinjadocs] in more depth. TL;DR:
 - [**Extending**][ext] another template allows you to override **blocks** that it provides for you to put content in
   - Example: `base.html.jinja2` (most pages either extend this or extend another page that extends this)
 - [**Including**][inc] another template renders its content and replaces the include block with it. Use this when you have content that can be re-used across pages, or is better understood in isolation from the context that it's in.
   - Example: `nav.html.jinja2` and `calendar.html.jinja2` are only used in `index.html.jinja2`, but moving them to separate files allows them to be understood more easily as they don't rely on the rest of `index.html.jinja2`.
 - [**Importing**][imp] from another template allows you to use **macros** or **variables** that template exports.
   - `base.html.jinja2` imports the macros from `utils.html.jinja2` so all templates that extend it can use them
   - `newslist.html.jinja2` defines a macro that both `index.html.jinja2` and `news.html.jinja2` use
     - This macro takes parameters to control the output, otherwise this would be a better fit for `include`.

## Macros vs filters &amp; functions
 - [**Macros**][macros] are written in Jinja and should be preferred over filters &amp; functions. They can take zero or more arguments.
   - Page-specific macros can be written outside a block, you may want these between the `title` and `body` blocks for consistency
   - Generic or re-used macros should be put in `utils.html.jinja2`, which will be inherited by all pages that extend `base.html.jinja2`
 - **Filters** are written in Python and should be used when you need to get information from Python, or if you need to do extensive processing on the argument(s) that's easier to read/write in Python than in Jinja. See [adding features in Python](adding_features_python.md). Filters take at least one argument.
 - **Functions** are just filters that take **no arguments**. They should be used when you want to get information from Python.

## Understanding the site template
All the pages on the website (excluding the server READMEs) inherit ultimately from `base.html.jinja2`. 

### Philosophy
The website is primarily for information, there's little use for dynamic pages so static HTML is used so we can take advantage of fast web servers and caching. Similarly on the front-end, few pages actually require JavaScript so we've avoided including frameworks. These priorities were true at the time of writing, but aren't set in stone; in the future some of these technologies may be an ideal solution to the requirements of the time. 

### Title
The code inside the `<title>` tag will always include `HackSoc - the computer science society`, but if a page has its own title, it'll put that first with a dash inbetween. Since title might be defined but have zero length, it's necessary to test `title|length>0`. This is jinja syntax for passing `title` to the filter `length`, it's equivalent to `length(title) > 0`.

In the future, the page title might be included on pages as `<h2>`. In order to do this, you could use `{{ title }}` to get the value of the `title` variable, or `{{ title() }}` to get the content of the `title` block. In this case it doesn't matter since they're equivalent.

### Metadata
This is a mess of [OpenGraph][ograph] (which most sites support) and [twitter-specific][twittercards] metadata. The main platforms to ensure compatibility and good display on are:
 - [Facebook](https://developers.facebook.com/docs/sharing/webmasters/#markup)
 - [Twitter][twittercards]
 - [Slack](https://api.slack.com/reference/messaging/link-unfurling#classic_unfurl)

Most pages are fairly generic, but news articles are more likely to be shared regularly, and also have more information that can be put into the metadata. Link embeds often look best with some kind of image included with them. Since the website doesn't use many photographs, some form of the logo will do. Note that Twitter and Facebook have different shapes for their embeds, if possible a different shaped logo for each would give the best display on each. 

The current implementation isn't perfect, if you think you can have a go at improving it, please do!

### CSS
The website uses fonts from Google Fonts and Roboto Slab, hosted directly. The latter appears to also be on Google Fonts; removing the font from the repository would simplify the license situation and possibly improve page loads (Google probably know what they're doing with regards to CDNs).

`hacksoc-colors.css` is taken from the [visual identity](https://github.com/HackSoc/visual-identity). It probably shouldn't be edited directly; if you want to change colours here then it's best to PR the visual identity repository and have that discussion there as it will have implications beyond the website.

`style_2017.css` contains the styles for everything else on the site. Where appropriate, it references colour variables from the visual identity.

There's also the `stylesheets` Jinja block where pages can add their own inline or external stylesheets. A similar block could be added for `<script>` tags if needed in the future. 

### "Body"
The *actual* content of the page is in `body > div#container > main`. In most cases this is referred to (admittedly confusingly) as the "body". The other elements inside `<body>` include the navbar, defined in `nav.html.jinja2`, the logo construction, the server list, and the footer.

The navbar has two copies of itself, one that's visible on the main site (desktop-first) and one that's visible on the mobile site. Ideally these could be merged into one; CSS should be more than sufficient to handle the differences. 

The server list pulls its items from the global context; this is passed by Flask to every template and pulled from `templates/context.yaml`.

The footer only contains details of our sponsorship by Bytemark. Bytemark is still providing us with two servers, one of which hosts the website itself, but the terms of this sponsorship are unclear, as there doesn't appear to be any requirement to display their logo on our site. Following their 2018 acquisition by iomart Group, anecdotes from those made redundant or chosing to leave paints a poor picture of the company, and in the future HackSoc may not want to display their logo on the site even if we are still using the servers.

#### Redirects
Page redirects are implemented by setting the `redirect` variable. Note that if this is set, the `body` block is not rendered at all, as it's replaced by a redirection notice. The value of the value is put into a meta-redirect tag. These can be full hyperlinks or relative links as necessary.

```html
{% extends "base.html.jinja2" %}

{% set redirect="/coc.html" %}
```



[jinjadocs]: https://jinja.palletsprojects.com/en/3.0.x/templates/ "Template designer documentation - Jinja Documentation (3.0.x)"
[ext]: https://jinja.palletsprojects.com/en/3.0.x/templates/#template-inheritance
[inc]: https://jinja.palletsprojects.com/en/3.0.x/templates/#include
[imp]: https://jinja.palletsprojects.com/en/3.0.x/templates/#import
[macros]: https://jinja.palletsprojects.com/en/3.0.x/templates/#macros
[ograph]: https://ogp.me/
[twittercards]: https://developer.twitter.com/en/docs/twitter-for-websites/cards/guides/getting-started