from flask import Blueprint, redirect, url_for

index_app = Blueprint(name="index_app", import_name=__name__, url_prefix="/", static_folder="../static")


@index_app.route("/", endpoint="root")
def root():
    url = url_for("articles_app.list")
    return redirect(url, code=308)
