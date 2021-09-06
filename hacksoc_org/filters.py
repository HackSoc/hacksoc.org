from hacksoc_org import app

@app.template_filter()
def example_filter(value):
    return "Hello, " + str(value) + "!"

# TODO: to use this in a jinja template, 