from time import time

from flask import Response, g


def before_request_timestamp():
    g.start_time = time()


def after_request_timestamp(response: Response):
    if hasattr(g, "start_time"):
        response.headers["X-Process-Time"] = time() - g.start_time
    return response
