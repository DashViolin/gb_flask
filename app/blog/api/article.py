from combojsonapi.event.resource import EventsResource
from flask_combo_jsonapi import ResourceDetail, ResourceList

from ..extensions import db
from ..models import Article
from ..permissions.article import ArticlePermission
from ..schemas import ArticleSchema


class ArticleListEvents(EventsResource):
    def event_get_count(self):
        return {"count": Article.query.count()}


class ArticleList(ResourceList):
    events = ArticleListEvents
    schema = ArticleSchema
    data_layer = {
        "session": db.session,
        "model": Article,
    }


class AuthorDetailEvents(EventsResource):
    def event_get_articles_count(self, **kwargs):
        return {"count": Article.query.filter(Article.author_id == kwargs["id"]).count()}


class ArticleDetail(ResourceDetail):
    events = AuthorDetailEvents
    schema = ArticleSchema
    data_layer = {
        "session": db.session,
        "model": Article,
        "permission_patch": [ArticlePermission],
    }
