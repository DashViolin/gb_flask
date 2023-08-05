from flask import Blueprint, redirect, url_for

index = Blueprint(name="index", import_name=__name__, url_prefix="/", static_folder="../static ")


@index.route("/", endpoint="root")
def root():
    url = url_for("articles.list")
    return redirect(url, code=308)
