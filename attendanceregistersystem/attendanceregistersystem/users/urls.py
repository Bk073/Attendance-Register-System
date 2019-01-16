from django.urls import path
from django.conf.urls import url

from attendanceregistersystem.users.views import (
    user_list_view,
    user_redirect_view,
    user_update_view,
    user_detail_view,
    user_login_view,
    user_create_view,
    user_logout_view,
    groups_create_view,
    permission_create_view,
    branch_list_view,
    groups_list_view,
)


app_name = "users"
urlpatterns = [
    # path("", view=user_list_view, name="list"),
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("update/<str:username>", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
    url(
        r'^v1/login/$',
        view=user_login_view,
        name="login"
    ),
    path("v1/create/", view= user_create_view, name="create-user"),
    path("v1/userlist/", view= user_list_view, name="list-user"),
    # url(
    #     r'^v1/logout/$',
    #     view = user_logout_view,
    #     name="logout"
    # ),
    path("v1/logout/", view= user_logout_view, name="logout"),
    path("v1/groups", view = groups_create_view, name="create-group"),
    path("v1/permission", view = permission_create_view, name="create-permission"),
    path("v1/branch", view =branch_list_view, name="branch_list"),
    path("v1/groupsList", view=groups_list_view, name="groups_list"),
]  
