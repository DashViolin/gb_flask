from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound

from ..models.article import Article

articles_app = Blueprint(name="articles_app", import_name=__name__, url_prefix="/articles", static_folder="../static")


@articles_app.route("/", endpoint="list")
def articles_list():
    published_articles = Article.query.filter_by(is_published=True)
    return render_template("articles/list.html", articles=published_articles)


@articles_app.route("/<int:pk>", endpoint="details")
def article_detail(pk: int):
    article = Article.query.filter_by(id=pk).one_or_none()
    if not article:
        raise NotFound(f"No such article with id={pk}")
    author = article.author
    return render_template("articles/detail.html", article=article, author=author)
