from flask import Blueprint, current_app, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from werkzeug.exceptions import NotFound

from ..extensions import db
from ..forms.articles import CreateArticleForm
from ..models import Author, Tag
from ..models.articles import Article

articles_app = Blueprint(name="articles_app", import_name=__name__, url_prefix="/articles", static_folder="../static")


@articles_app.route("/", endpoint="list")
def articles_list():
    if hasattr(current_user, "is_staff") and current_user.is_staff:
        published_articles = Article.query.all()
    else:
        published_articles = Article.query.filter_by(is_published=True)
    return render_template("articles/list.html", articles=published_articles)


@articles_app.route("/<int:pk>", endpoint="details")
def article_detail(pk: int):
    article = Article.query.filter_by(id=pk).options(joinedload(Article.tags)).one_or_none()
    if not article:
        raise NotFound(f"No such article with id={pk}")
    author = article.author
    return render_template("articles/detail.html", article=article, author=author)


@articles_app.route("/create/", methods=["GET", "POST"], endpoint="create")
@login_required
def create_article():
    errors = []
    form = CreateArticleForm(request.form)
    form.tags.choices = [(tag.id, tag.name) for tag in Tag.query.order_by("name")]
    if request.method == "POST" and form.validate_on_submit():
        if not current_user.author:
            author = Author(user_id=current_user.id)
            db.session.add(author)
        else:
            author = current_user.author
        article = Article(title=form.title.data.strip(), summary=form.summary.data, body=form.body.data)
        article.author = author
        if form.tags.data:
            selected_tags = Tag.query.filter(Tag.id.in_(form.tags.data))
            for tag in selected_tags:
                article.tags.append(tag)
        db.session.add(article)
        try:
            db.session.commit()
        except IntegrityError as ex_msg:
            msg = f"Could not create a new article! ({ex_msg})"
            current_app.logger.exception(msg)
            errors.append(msg)
        else:
            return redirect(url_for("articles_app.details", pk=article.id))
    return render_template("articles/create.html", form=form, errors=errors)
