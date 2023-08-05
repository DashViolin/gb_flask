from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound

from ..db.data_mock import ARTICLES, USERS

article = Blueprint(name="article", import_name=__name__, url_prefix="/article", static_folder="../static ")


@article.route("/")
def articles_list():
    return render_template("articles/list.html", articles=ARTICLES, active_page="articles")


@article.route("/<int:pk>")
def article_detail(pk: int):
    article_obj = ARTICLES.get(pk)
    author = USERS.get(article_obj["author_id"])
    if article_obj:
        return render_template("articles/detail.html", article=article_obj, author=author, active_page="articles")
    raise NotFound
