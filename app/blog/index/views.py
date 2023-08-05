from flask import Blueprint, redirect, url_for

index = Blueprint(name="index", import_name=__name__, url_prefix="/", static_folder="../static ")


@index.route("/")
def index_view():
    return redirect(url_for("article.articles_list"), code=308)
