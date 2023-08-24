from blog.models import Author
from flask import Blueprint, render_template

authors_app = Blueprint("authors_app", import_name=__name__, url_prefix="/authors", static_folder="../static")


@authors_app.route("/", endpoint="list")
def authors_list():
    authors = Author.query.all()
    return render_template("authors/list.html", authors=authors)


@authors_app.route("/<int:pk>", endpoint="details")
def author_detail(pk: int):
    author = Author.query.get_or_404(pk)
    return render_template("authors/detail.html", author=author)
