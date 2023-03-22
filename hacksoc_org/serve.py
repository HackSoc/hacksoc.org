"""
    Provides a simple static HTTP server for local testing
"""

import http.server
import functools


def serve(basedir: str, port=5000):
    """Starts a local HTTP server on port 5000, such that `basedir` + index.html appears at '/'

    Args:
        basedir (str): Path to the web root directory
    """

    print(f"Serving {basedir} at http://127.0.0.1:{port}/ ...")

    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=basedir)
    server = http.server.HTTPServer(("localhost", port), RequestHandlerClass=handler)
    server.serve_forever()
