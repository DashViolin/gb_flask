from time import time

from flask import Flask, Response, g, request

app = Flask(__name__)


@app.route("/<string:parameter>", methods=["GET", "POST"])
def index(parameter: str):
    query_string = f"<br/>Query: {request.query_string.decode('utf8')}" if request.query_string else ""
    content = f"<p>Hello!<br/>Param: {parameter}{query_string}<p>"
    return Response(f"<html><head></head><body>{content}</body></html>")


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


@app.errorhandler(ZeroDivisionError)
def handle_zero_division_error(error):
    app.logger.exception(error)
    return "Error!", 500
