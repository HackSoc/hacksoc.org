from datetime import date
from logging import root
import re
from typing import Dict

from flask.helpers import url_for
from hacksoc_org import app, root_dir

from hacksoc_org.markdown import render_markdown

from flask import get_template_attribute

import os
from pprint import pformat
from operator import itemgetter

@app.template_filter()
def example_filter(value):
    return "Hello, " + str(value) + "!"

@app.template_filter()
def paginate(indexable,start, count):
    if count > 0:
        return indexable[start:start+count]
    else:
        return indexable[start:]

@app.template_global()
def get_news():
    news = []
    for filename in os.listdir(os.path.join(root_dir, "templates", "content", "news")):
        if filename.endswith(".md"):
            template_name = os.path.join("content","news",filename.removesuffix(".md") + ".html.jinja2")
        else:
            template_name = os.path.join("content","news",filename)
        title = get_template_attribute(template_name, "title")
        lede = get_template_attribute(template_name, "lede")
        published = date.fromisoformat(filename[:10])
        news.append({
            'title': title.strip(),
            'lede': lede.strip(),
            'date': published,
            'url': url_for('.render_news', article=filename.removesuffix(".md").removesuffix(".html.jinja2"))
        })
        if len(lede) == 0:
            print("No lede found for", filename)
    news.sort(key=itemgetter("date"), reverse=True)
    return news

@app.template_filter()
def pretty(arg):
    return pformat(arg)

@app.template_filter()
def markdown(caller):
    return render_markdown(caller)

@app.template_filter()
def split_lede(caller) -> Dict[str,str]:
    lede_re = re.compile(r"^\s*<p>(.*?)</p>", flags=re.DOTALL)
    match = lede_re.match(caller)

    if match is None:
        print(caller)
        return {'lede': '', 'text': caller}
    else:
        return {'lede': match[1], 'text': caller[match.end(0):]}

months = [
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
    "December"
]

@app.template_filter()
def format_date(d : date):
    if not isinstance(d,date):
        # this can happen when calling get_template_attribute on an article
        # since the date doesn't get passed to the template at that point, only in the render_article route.
        return str(d)
    else:
        return f"{months[d.month-1]} {d.day:02d}, {d.year}"