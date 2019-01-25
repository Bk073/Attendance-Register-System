from django.urls import path
from django.conf.urls import url
from .views import PasswordResetView, reset_confirm

app_name = "resetPassword"

urlpatterns = [
    # path("", view=user_list_view, name="list"),
    url(r'^password/reset/confirm/(?P<uid>[\w-]+)/(?P<token>[\w-]+)/$', PasswordResetView.as_view()),
    #reset/password/reset/confirm/{uid}/{token}
]