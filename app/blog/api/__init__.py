from combojsonapi.spec import ApiSpecPlugin
from flask_combo_jsonapi import Api

from .article import ArticleDetail, ArticleList
from .author import AuthorDetail, AuthorList
from .tag import TagDetail, TagList
from .user import UserDetail, UserList


def create_api_spec_plugin(app):
    return ApiSpecPlugin(
        app=app,
        tags={
            "Tag": "Tag API",
            "User": "User API",
            "Author": "Author API",
            "Article": "Article API",
        },
    )


def init_api(app):
    api_spec_plugin = create_api_spec_plugin(app)
    api = Api(
        app,
        plugins=[
            api_spec_plugin,
        ],
    )
    api.route(TagList, "tag_list", "/api/tags/", tag="Tag")
    api.route(TagDetail, "tag_detail", "/api/tags/<int:id>/", tag="Tag")
    api.route(UserList, "user_list", "/api/users/", tag="User")
    api.route(UserDetail, "user_detail", "/api/users/<int:id>/", tag="User")
    api.route(ArticleList, "article_list", "/api/article/", tag="Article")
    api.route(ArticleDetail, "article_detail", "/api/article/<int:id>/", tag="Article")
    api.route(AuthorList, "author_list", "/api/authors/", tag="Author")
    api.route(AuthorDetail, "author_detail", "/api/authors/<int:id>/", tag="Author")
