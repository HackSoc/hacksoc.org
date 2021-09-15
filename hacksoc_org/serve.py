"""
    Provides a simple static HTTP server for local testing
"""

# http.server doesn't export `test`, this may be a bit dodgy to rely on
from http.server import test, SimpleHTTPRequestHandler

import functools

def serve(basedir : str):
    """Starts a local HTTP server on port 5000, such that `basedir` + index.html
    appears at '/'

    Args:
        basedir (str): Path to the web root directory
    """
    test(HandlerClass=functools.partial(SimpleHTTPRequestHandler, directory=basedir), port=5000)
