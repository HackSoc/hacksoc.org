from hacksoc_org import app

@app.template_filter()
def example_filter(value):
    return "Hello, " + str(value) + "!"

@app.template_filter()
def paginate(start, count, indexable):
    if count > 0:
        return indexable[start:start+count]
    else:
        return indexable[start:]