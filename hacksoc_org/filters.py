from logging import root
from hacksoc_org import app, root_dir

from hacksoc_org.markdown import render_markdown

import os

@app.template_filter()
def example_filter(value):
    return "Hello, " + str(value) + "!"

@app.template_filter()
def paginate(start, count, indexable):
    if count > 0:
        return indexable[start:start+count]
    else:
        return indexable[start:]

@app.template_global()
def get_news():
    news = []
    for filename in os.listdir(os.path.join(root_dir, "templates", "content", "news")):
        pass
    return news

from pprint import pp

@app.template_filter()
def markdown(caller):
    return render_markdown(caller)