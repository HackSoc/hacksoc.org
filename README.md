HackSoc.org
===

![Unit test status badge](https://github.com/hacksoc/hacksoc.org/actions/workflows/unittest.yaml/badge.svg)

This build system is written in Python, [Flask](https://flask.palletsprojects.com/en/2.0.x/) and [Jinja](https://jinja.palletsprojects.com/en/3.0.x/). It replaces the [previous system][tag-previous] which used Node.js and [Handlebars](https://handlebarsjs.com/), in turn replacing the [system before it][tag-hackyll] based on Haskell and [Hakyll](https://jaspervdj.be/hakyll/).

## Documentation
Documentation can be found in [`docs/`](docs/), including topics such as:

|                                                                                           |
|-------------------------------------------------------------------------------------------|
| [Writing news articles](docs/writing_articles.md)                                         |
| [Creating &amp; modifying **simple** pages](docs/creating_modifying_simple_pages.md)      |
| [Creating &amp; modifying **complex** pages](docs/creating_modifying_complex_pages.md)    |
| [Adding features in Python &ndash; advanced](docs/adding_features_python.md)              |
| [Adding meeting minutes](docs/minutes.md)                                                 |
| [Writing server READMEs](docs/servers.md)                                                 |
| [Development process and using git &ndash; beginner's guide](docs/development_and_git.md) |

## Running
Preferred way to run is through the `hacksoc_org` command. It can be executed with the venv (see [Installation](#installation)) activated by just running `hacksoc_org` (all platforms, recommended) or otherwise at `venv/bin/hacksoc_org` on Mac and Linux.

Note that running through `flask run` is **not supported**.

### Starting a development server
While you're developing, you probably want to use:
```
hacksoc_org run
```
Pages are served directly from the Flask routes; you shouldn't need to restart the server when changes are made, but web pages will not automatically refresh. Open your browser to [`http://localhost:5000/`](http://localhost:5000/) to see the results.

### Freezing to HTML
To produce a folder full of static HTML and assets (images, CSS, JS, fonts), the site must be *frozen*. The resulting folder can then be used with a regular webserver (like nginx), and should look exactly the same as when running with `hacksoc_org run`. You probably want to use this or `hacksoc_org serve` at least once before you create a pull request.
```
hacksoc_org run
```
The HTTP root directory is `build/`.

### Starting a static server
```
hacksoc_org serve
```
Starts a local HTTP server from the `build/` directory. Equivalent to running `hacksoc_org freeze` followed by `cd build/ && python3 -m http.server 5000`. If all goes well, you should always see the same as `hacksoc_org run`.

## Style guide
To keep a consistent style, the following rules are used:

### Line length
 - **Markdown** files:
   - News articles should not exceed **70 characters** per line
 - **Python** files:
   - **100 characters** per line (use `black hacksoc_org` to apply formatting automatically)

Otherwise, there is no line length limit, and you are encouraged to use "soft wrap" features in your editor.

### Code style
Python files should roughly follow [PEP 8](https://www.python.org/dev/peps/pep-0008/), formatted with `black`. 

Note that although constants should be in uppercase, PEP 8 does not strictly define what counts as a constant. Some variables in `hacksoc_org/` are assigned once and should never be reassigned, but are mutated often and generally don't behave like constants (for example `app`, `blueprint` from Flask). When considering whether to name a variable as a constant, think about the following:
 - Could the variable be replaced with its literal value?
 - Does the value of the variable ever change? (this includes mutations rather than just reassignments)
### Years of study
[about.html](templates/content/about.html.jinja2) contains information about the committee, including their current year of study. The year given should be the 'stage' that the committee member is in. When a member is on a year in industry, they should not be listed as being in any year and instead as "currently on year in industry". If the year in industry is in between stages two and three, they will return as a "third year".

More style guidance may be added so always check this section when authoring new content!

## Installation

After you've cloned the repository, create a new **virtual environment** with the following:
```
python3.7 -m venv venv/
```
Note that the **minimum supported version is Python 3.7**; if possible, try not to introduce code which requires Python 3.8 or higher. If you're using Ubuntu 18.04 LTS, you can use the [deadsnakes](https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa) PPA to access more recent versions of Python.

Next install dependencies
```
# For Linux/MacOS and Windows Subsystem for Linux (WSL) users
source venv/bin/activate

# Windows users using cmd.exe
venv\Scripts\activate.bat

# Windows users using PowerShell
venv\Scripts\Activate.ps1

pip install --upgrade pip
pip install -e .

# If and only if you are using an Apple Silicon-based Mac, you must also install a non-pre-built pygit2
# (Requires Homebrew)
brew install libgit2
pip uninstall pygit2
pip install pygit2 --no-binary pygit2
```

On existing installations, if Python throws `ModuleNotFoundError`s, try running `pip install -e .` again as additional dependencies may have been added since your original install.

See [Running](#running) next.

## License
Currently this repository has **no license** ([#150](https://github.com/HackSoc/hacksoc.org/issues/150)). This means that the effective license is **All rights reserved**. 

Exceptions to this license include the fonts in `static/fonts`, which are licensed under the Apache license (found at [`static/fonts/Apache License.txt`](static/fonts/Apache%20License.txt)):
 - Bitstream Vera Sans
 - DejaVu Sans Condensed
 - Roboto Slab (Bold and Regular)

The Bytemark name and logo (`static/images/bytemark.png`) are registered trademarks of Bytemark Limited.

[tag-previous]: https://github.com/HackSoc/hacksoc.org/tree/node-last
[tag-hackyll]: https://github.com/HackSoc/hacksoc.org/tree/hakyll-last
