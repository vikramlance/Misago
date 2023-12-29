from django.urls import path
from django.contrib import admin as djadmin
from django.contrib.auth import get_user_model
from django.utils.translation import pgettext_lazy

from .djangoadmin import UserAdminModel
from .views.bans import BansList, DeleteBan, EditBan, NewBan
from .views.datadownloads import DataDownloadsList, RequestDataDownloads
from .views import groups
from .views.ranks import (
    DefaultRank,
    DeleteRank,
    EditRank,
    MoveDownRank,
    MoveUpRank,
    NewRank,
    RanksList,
    RankUsers,
)
from .views.users import EditUser, NewUser, UsersList

djadmin.site.register(model_or_iterable=get_user_model(), admin_class=UserAdminModel)


class MisagoAdminExtension:
    def register_urlpatterns(self, urlpatterns):
        # Users section
        urlpatterns.namespace("users/", "users")

        # Accounts
        urlpatterns.patterns(
            "users",
            path("", UsersList.as_view(), name="index"),
            path("<int:page>/", UsersList.as_view(), name="index"),
            path("new/", NewUser.as_view(), name="new"),
            path("edit/<int:pk>/", EditUser.as_view(), name="edit"),
        )

        # Bans
        urlpatterns.namespace("bans/", "bans", "users")
        urlpatterns.patterns(
            "users:bans",
            path("", BansList.as_view(), name="index"),
            path("<int:page>/", BansList.as_view(), name="index"),
            path("new/", NewBan.as_view(), name="new"),
            path("edit/<int:pk>/", EditBan.as_view(), name="edit"),
            path("delete/<int:pk>/", DeleteBan.as_view(), name="delete"),
        )

        # Data Downloads
        urlpatterns.namespace("data-downloads/", "data-downloads", "users")
        urlpatterns.patterns(
            "users:data-downloads",
            path("", DataDownloadsList.as_view(), name="index"),
            path("<int:page>/", DataDownloadsList.as_view(), name="index"),
            path("request/", RequestDataDownloads.as_view(), name="request"),
        )

        # Groups section
        urlpatterns.namespace("groups/", "groups")
        urlpatterns.patterns(
            "groups",
            path("", groups.ListView.as_view(), name="index"),
            path("ordering/", groups.OrderingView.as_view(), name="ordering"),
            path("new/", groups.NewView.as_view(), name="new"),
            path("edit/<int:pk>/", groups.EditView.as_view(), name="edit"),
            path(
                "categories/<int:pk>/",
                groups.CategoryPermissionsView.as_view(),
                name="categories",
            ),
            path("default/<int:pk>/", groups.MakeDefaultView.as_view(), name="default"),
            path("members/<int:pk>/", groups.MembersView.as_view(), name="members"),
            path(
                "members-main/<int:pk>/",
                groups.MembersMainView.as_view(),
                name="members-main",
            ),
            path("delete/<int:pk>/", groups.DeleteView.as_view(), name="delete"),
        )

        # Ranks
        urlpatterns.namespace("ranks/", "ranks")
        urlpatterns.patterns(
            "ranks",
            path("", RanksList.as_view(), name="index"),
            path("new/", NewRank.as_view(), name="new"),
            path("edit/<int:pk>/", EditRank.as_view(), name="edit"),
            path("default/<int:pk>/", DefaultRank.as_view(), name="default"),
            path("move/down/<int:pk>/", MoveDownRank.as_view(), name="down"),
            path("move/up/<int:pk>/", MoveUpRank.as_view(), name="up"),
            path("users/<int:pk>/", RankUsers.as_view(), name="users"),
            path("delete/<int:pk>/", DeleteRank.as_view(), name="delete"),
        )

    def register_navigation_nodes(self, site):
        site.add_node(
            name=pgettext_lazy("admin node", "Users"),
            icon="fa fa-users",
            after="index",
            namespace="users",
        )

        site.add_node(
            name=pgettext_lazy("admin node", "Bans"),
            parent="users",
            namespace="bans",
        )

        site.add_node(
            name=pgettext_lazy("admin node", "Data downloads"),
            parent="users",
            after="bans:index",
            namespace="data-downloads",
        )

        site.add_node(
            name=pgettext_lazy("admin node", "Groups"),
            icon="fas fa-adjust",
            after="users:index",
            namespace="groups",
        )

        site.add_node(
            name=pgettext_lazy("admin node", "Ranks"),
            icon="fas fa-shield-alt",
            after="groups:index",
            namespace="ranks",
        )
