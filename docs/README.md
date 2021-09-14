# Website and build system documentation

Documentation is never complete; if you see a section that's missing information, please make an issue. If over the course of working with the website you discover something that might not be immediately clear to everyone, consider making a pull request adding it to the documentation so fewer people get tripped up on it in the future!

## What you need to read

|                                                                                      |
|--------------------------------------------------------------------------------------|
| [Writing news articles](writing_articles.md)                                         |
| [Creating &amp; modifying **simple** pages](creating_modifying_simple_pages.md)      |
| [Creating &amp; modifying **complex** pages](creating_modifying_complex_pages.md)    |
| [Adding features in Python &ndash; advanced](adding_features_python.md)              |
| [Adding meeting minutes](minutes.md)                                                 |
| [Writing server READMEs](servers.md)                                                 |
| [Development process and using git &ndash; beginner's guide](development_and_git.md) |


## Folder structure

 - `hacksoc_org/`: Python package for the build system
 - `static/`: files that are served as-is, and will rarely (if ever) change, suitable for caching
   - `fonts/`: font and relevant files (such as font stylesheets)
   - `images/`: images, logos, and favicons
   - `js/`: `.js` scripts
   - `minutes/` meeting minutes in PDF format
   - CSS files are kept (currently) in the root of `static/`
 - `templates/`: top level contains templates that don't directly produce a page
   - `content/`: every file in this level maps 1:1 with a produced HTML page
     - `news/`: `.md` and `.html.jinja2` files for news articles.
     - `servers/`: `.md` files for server READMEs