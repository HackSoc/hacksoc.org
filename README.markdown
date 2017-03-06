Building
========

Set-up
------

1. Install [stack](https://github.com/commercialhaskell/stack).
2. If you don't have GHC 8.0.2, run `stack setup`

Build Site Generator
--------------------

This can be skipped on subsequent executions unless you edit `hakyll.hs`

1. `stack build`

This will install a lot of dependencies the first time because Haskell projects always have lots of
dependencies.

*Note:* you may run out of disk space in the `stack build` if you have a very small `/tmp` (or
`/run`, depending on how things are set up). `stack` will complain at you and delete its temporary
files. If you run it again, `stack build` will then pick up where it left off, without rebuilding
the dependencies it already built, so you should be good.

Build Site
----------

1. `stack exec hacksoc-org build`

You can use `stack exec hacksoc-org clean` to remove the generated files, or just delete `_cache`
and `_site` yourself.


Usage
=====

This is a summary of `hakyll.hs` in plain English.

- Templates (in `templates/`) control how things look. There are currently three:
    - `news.html` renders a single news article.
    - `newslist.html` renders a list of news articles, and includes the index page content currently
      (as we want that to appear on every list page).
    - `wrapper.html` is applied to every rendered page and contains the header and footer.
- Files in `static/` are copied straight to the site, with the `static/` prefix dropped (so
  `static/foo` becomes accessible at `hacksoc.org/foo`).
- Articles in `news/` appear on the main page and the news pages. See current entries for the
  format.
- All `.html` files are wrapped.
