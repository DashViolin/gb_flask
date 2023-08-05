from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound

from ..db.data_mock import ARTICLES, USERS

articles = Blueprint(name="articles", import_name=__name__, url_prefix="/articles", static_folder="../static ")


@articles.route("/", endpoint="list")
def articles_list():
    return render_template("articles/list.html", articles=ARTICLES)


@articles.route("/<int:pk>", endpoint="details")
def article_detail(pk: int):
    article_obj = ARTICLES.get(pk)
    author = USERS.get(article_obj["author_id"])
    if not article_obj:
        raise NotFound(f"No such article with id={pk}")
    if not author:
        raise NotFound(f"No such user with id={article_obj['author_id']}")
    return render_template("articles/detail.html", article=article_obj, author=author)
