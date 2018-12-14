from django.urls import path
from django.conf.urls import url

from attendanceregistersystem.users.views import (
    user_list_view,
    user_redirect_view,
    user_update_view,
    user_detail_view,
    user_login_view,
)

app_name = "users"
urlpatterns = [
    path("", view=user_list_view, name="list"),
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
    url(
        r'^v1/login/$',
        view=user_login_view,
        name="login"
    )
    #path('api/login', login)
]   