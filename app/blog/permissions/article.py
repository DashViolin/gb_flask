from combojsonapi.permission.permission_system import (
    PermissionForGet,
    PermissionForPatch,
    PermissionMixin,
    PermissionUser,
)
from flask_combo_jsonapi.exceptions import AccessDenied
from flask_login import current_user

from ..models import Article


class ArticlePermission(PermissionMixin):
    ALL_AVAILABLE_FIELDS = [
        "id",
        "title",
        "summary",
        "body",
        "created_at",
        "updated_at",
        "is_published",
        "author_id",
    ]
    PATCH_AVAILABLE_FIELDS = [
        "title",
        "summary",
        "body",
        "is_published",
    ]

    def get(self, *args, many=True, user_permission: PermissionUser = None, **kwargs) -> PermissionForGet:
        """
        Set available columns
        :param args:
        :param many:
        :param user_permission:
        :param kwargs:
        :return:
        """
        self.permission_for_get.allow_columns = (self.ALL_AVAILABLE_FIELDS, 10)
        return self.permission_for_get

    def patch_permission(self, *args, user_permission: PermissionUser = None, **kwargs) -> PermissionForPatch:
        self.permission_for_patch.allow_columns = (self.PATCH_AVAILABLE_FIELDS, 10)
        return self.permission_for_patch

    def patch_data(
        self, *args, data: dict = None, obj: Article = None, user_permission: PermissionUser = None, **kwargs
    ) -> dict:
        if not current_user.is_authenticated:
            raise AccessDenied("no access")

        author = Article.query.get(data["id"]).author
        if current_user.id != author.id or not current_user.is_staff:
            raise AccessDenied("no access")

        permission_for_patch = user_permission.permission_for_patch_permission(model=Article)
        return {i_key: i_val for i_key, i_val in data.items() if i_key in permission_for_patch.columns}
