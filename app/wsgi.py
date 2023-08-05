from time import time

from blog.app import create_app
from flask import Response, g

app = create_app()


@app.before_request
def before_request():
    g.start_time = time()


@app.after_request
def after_request(response: Response):
    if hasattr(g, "start_time"):
        response.headers["X-Process-Time"] = time() - g.start_time
    return response


@app.errorhandler(404)
def handler_404(error_msg):
    app.logger.error(error_msg)
    return "Not found!", 404


@app.errorhandler(Exception)
def handle_zero_division_error(error):
    app.logger.exception(error)
    return "Error!", 500


if __name__ == "__main__":
    app.run()
