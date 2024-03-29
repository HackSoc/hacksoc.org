"""
    Function definitions for custom Jinja filters and functions.

    Functions are decorated and add themselves to the Flask context at import
    time. This file must be imported after hacksoc_org.app is defined.
"""

import datetime
from flask import get_template_attribute

import yaml

from datetime import date, timedelta, timezone
from email.utils import format_datetime as rfc_822_format_datetime
import re
import os
from pprint import pformat
from operator import itemgetter

from typing import Any, Dict, List, Union

from hacksoc_org import app, ROOT_DIR
from hacksoc_org.markdown import render_markdown
from hacksoc_org.util import removesuffix

from pygit2 import Commit
from hacksoc_org.git import REPO


@app.template_filter()
def paginate(indexable, start: int, count: int):
    """Splits `indexable` into chunks of `count` elements starting with the
    `start`th element.

    Args:
        indexable: sequential collection that supports indexing and slicing (in most cases List)
        start (int): index of the first element to return
        count (int): total (maxiumum) number of elements to return.

    Returns:
        up to `count` elements from indexable starting at `start`.
    """
    if count > 0:
        return indexable[start : start + count]
    else:
        return indexable[start:]


@app.template_global()
def get_news() -> List[Dict[str, Any]]:
    """Gets the context for the newslist from the article files in `news/`

    Returns:
        List[Dict[str, any]]: One Dict per news article with keys and values:
            `title` (str): article title (plain text)
            `lede` (str): article lede (HTML)
            `date` (datetime.date): date of initial publication
            `article_name`: filename of the article file (Jinja or Markdown)
            with the extension removed.
    """
    news = []
    for filename in os.listdir(os.path.join(ROOT_DIR, "templates", "content", "news")):
        if filename.endswith(".md"):
            template_name = os.path.join(
                "content", "news", removesuffix(filename, ".md") + ".html.jinja2"
            )
        else:
            template_name = os.path.join("content", "news", filename)
        title = get_template_attribute(template_name, "title")
        lede = get_template_attribute(template_name, "lede")
        published = date.fromisoformat(filename[:10])
        news.append(
            {
                "title": title.strip(),
                "lede": lede.strip(),
                "date": published,
                "article_name": removesuffix(removesuffix(filename, ".md"), ".html.jinja2"),
            }
        )
        if len(lede) == 0:
            print("No lede found for", filename)
    news.sort(key=itemgetter("date"), reverse=True)
    return news


@app.template_filter()
def pretty(arg: Any) -> str:
    """Returns `arg` as it would be printed by `pprint`

    Args:
        arg (any):

    Returns:
        str: pretty-print representation of `arg`. Useful for debugging, often
        looks best in monospace/preformatted blocks.
    """
    return pformat(arg)


@app.template_filter()
def markdown(caller):
    """Renders the argument to markdown. Useful in `{% filter markdown() %} `
    blocks

    Args:
        caller (str): Markdown source

    Returns:
        str: rendered HTML
    """
    return render_markdown(caller)


@app.template_filter()
def from_yaml(caller: str) -> Union[List, Dict]:
    """Parses the argument as YAML. Useful for quickly defining data to pass to Jinja macros to
    template.

    ```
    {% set events | from_yaml %}
        - name: Boardgames and Cake
          desc: >
            In one of the oldest and noblest traditions of HackSoc, we descend upon a room, play
            many boardgames, and eat much cake. Both boardgames and cake are brought along by
            members, so if you do enjoy the events, please consider bringing something along.
        - name: CoffeeScript
          desc: >
            An unprecedented case of joviality and camaraderie has struck HackSoc, and we have
            responded with a weekly social over in the Ron Cooke Hub cafe on Hes East. Come for
            lunch, a chat, and maybe a small game or two.
    {% endset %}

    {% for item in events %}
        <section class="event">
            <h2> {{ item.name }} </h2>
            <p> {{ item.desc }} </p>
        </section>
    {% endfor %}
    ```

    Args:
        caller (str): YAML source, usually from a Jinja block (eg block assignment or macro call
        block)

    Returns:
        Union[List, Dict]: YAML supports top-level lists or dictionaries (objects).
    """
    return yaml.safe_load(caller)


@app.template_filter()
def split_lede(caller) -> Dict[str, str]:
    """Parses HTML with regular expressions.

    Splits the first paragraph of a news article from the rest of the article. Assumes that caller
    starts with a <p> block and no other (non-whitespace) characters.

    Args:
        caller (str): HTML source beginning with a <p> block

    Returns:
        Dict[str,str]:
            `lede`: First <p> of `caller`, **excluding** the surrounding tags
            `text`: Rest of the article (everything after the first </p>)
    """
    lede_re = re.compile(r"^\s*<p>(.*?)</p>", flags=re.DOTALL)
    match = lede_re.match(caller)

    if match is None:
        print(caller)
        return {"lede": "", "text": caller}
    else:
        return {"lede": match[1], "text": caller[match.end(0) :]}


MONTHS = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


@app.template_filter()
def with_ordinal_indicator(n: int):
    if not isinstance(n, int):
        return n
    else:
        # https://leancrew.com/all-this/2020/06/ordinals-in-python/
        strings = ("th", "st", "nd", "rd") + ("th",) * 10
        v = n % 100
        if v > 13:
            return f"{n}{strings[v%10]}"
        else:
            return f"{n}{strings[v]}"


@app.template_filter()
def format_date(d: date, year=True):
    """Formats dates as "January 02, 2021"

    Args:
        d (date): Python datetime.date object
        year (bool): Whether to include the year (default: True)

    Returns:
        str: formatted date
    """
    if not isinstance(d, date):
        # this can happen when calling get_template_attribute on an article
        # since the date doesn't get passed to the template at that point, only in the
        # render_article route.
        return str(d)
    else:
        s = f"{with_ordinal_indicator(d.day)} {MONTHS[d.month-1]}"
        if year:
            s += f", {d.year}"
        return s


@app.template_global()
def build_datetime():
    """Returns the current datetime (to seconds precision)

    Returns:
        datetime: current Python datetime object
    """
    return datetime.datetime.now(timezone.utc).astimezone().replace(microsecond=0)


@app.template_filter()
def from_iso_date(s: str):
    """Converts an ISO format datestring to a date object

    Args:
        s (str): YYYY-MM-DD date string

    Returns:
        date: Python datetime.date object
    """

    if isinstance(s, date):
        return s
    elif s is None:
        return None
    else:
        print(type(s))

    return date.fromisoformat(s)


@app.template_global()
def git_head() -> Commit:
    """Returns the commit at HEAD

    https://www.pygit2.org/objects.html#commits
    Returns:
        Commit: pygit2 Commit object
    """
    return REPO[REPO.head.target]


@app.template_filter()
def git_date(commit: Commit) -> datetime.datetime:
    """Wrangles a datetime out of a Commit.

    Args:
        commit (Commit): PyGit2 Commit object

    Returns:
        datetime: Commit time.
    """
    return datetime.datetime.fromtimestamp(
        commit.commit_time, datetime.timezone(timedelta(minutes=commit.commit_time_offset))
    )


@app.template_filter()
def commit_to_url(full_commit_hash: str) -> str:
    """Provides a remote URL (eg. for GitHub) for a given commit ID

    Args:
        full_commit_hash (str): commit ID

    Returns:
        str: URL
    """
    return f"https://github.com/hacksoc/hacksoc.org/commit/{full_commit_hash}"


def _to_utc_datetime(to_convert: Union[datetime.datetime, datetime.date]) -> datetime.datetime:
    """Convert a date or datetime to a datetime in UTC with midnight set if no time exists.

    Args:
        to_convert (datetime.datetime|datetime.date): date to convert

    Returns:
        datetime.datetime: the converted datetime
    """
    # datetime is a subclass of date so we need to do this backwards comparison
    # so only date matches and not datetime
    if not isinstance(to_convert, datetime.datetime):
        to_convert = datetime.datetime(to_convert.year, to_convert.month, to_convert.day)

    # if we have a "naive" date e.g. one without timezone
    if to_convert.tzinfo is None or to_convert.tzinfo.utcoffset(to_convert) is None:
        to_convert = to_convert.replace(tzinfo=timezone.utc)

    return to_convert


@app.template_filter()
def to_rfc_822_date(to_convert: Union[datetime.datetime, datetime.date]) -> str:
    """Get an RFC-822 formatted date string for a python datetime.

    Args:
        to_convert (datetime.datetime|datetime.date): date to convert

    Returns:
        str: formatted date
    """
    to_convert = _to_utc_datetime(to_convert)

    # the email module has a function for this format as it's also used in email
    return rfc_822_format_datetime(to_convert)


@app.template_filter()
def to_rfc_3339_date(to_convert: Union[datetime.datetime, datetime.date]) -> str:
    """Get an RFC-3339 formatted date string for a python datetime.

    Args:
        to_convert (datetime.datetime|datetime.date): date to convert

    Returns:
        str: formatted date
    """
    to_convert = _to_utc_datetime(to_convert)

    # the `datetime.isoformat()` method is already RFC-3339 compatible as long
    # as the datetime is not naive and has a time component.
    return to_convert.isoformat()
