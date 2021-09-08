from http.server import test, SimpleHTTPRequestHandler

import functools

def serve(basedir):
    test(HandlerClass=functools.partial(SimpleHTTPRequestHandler, directory=basedir), port=5000)
