import pytest
from django.conf import settings
from django.test import RequestFactory
from rest_framework import status

from attendanceregistersystem.users.views import UserRedirectView, UserUpdateView, UserLoginView, UserCreateView
pytestmark = pytest.mark.django_db


class TestUserUpdateView:
    """
    TODO:
        extracting view initialization code as class-scoped fixture
        would be great if only pytest-django supported non-function-scoped
        fixture db access -- this is a work-in-progress for now:
        https://github.com/pytest-dev/pytest-django/pull/258
    """

    def test_get_success_url(
        self, user: settings.AUTH_USER_MODEL, request_factory: RequestFactory
    ):
        view = UserUpdateView()
        request = request_factory.get("/fake-url/")
        request.user = user

        view.request = request

        assert view.get_success_url() == f"/users/{user.username}/"

    def test_get_object(
        self, user: settings.AUTH_USER_MODEL, request_factory: RequestFactory
    ):
        view = UserUpdateView()
        request = request_factory.get("/fake-url/")
        request.user = user

        view.request = request

        assert view.get_object() == user


class TestUserRedirectView:

    def test_get_redirect_url(
        self, user: settings.AUTH_USER_MODEL, request_factory: RequestFactory
    ):
        view = UserRedirectView()
        request = request_factory.get("/fake-url")
        request.user = user

        view.request = request

        assert view.get_redirect_url() == f"/users/{user.username}/"


class TestLoginView:

    def test_user_login_token(
        self, user: settings.AUTH_USER_MODEL, request_factory: RequestFactory
    ):
        view = UserLoginView()
        request = request_factory.get("/fake-url")
        request.user = user

        view.request = request
        assert view.post(request) == f""


class TestUserCreateView:
    def test_create_method(self, user: settings.AUTH_USER_MODEL, request_factory: RequestFactory):
        view = UserCreateView
        request = request_factory.post("/fake-url")
        request.user = user

        view.request = request
        assert view.create(request) == status.HTTP_201_CREATED

        
# wrong data should raise exception, status code should be 4XX
# right data should give correct token key, status should be 200
# token if doesnt exist, should be created for the user
# token if exists already, it should return that token and in successive calls
# not-existing user should throw error
# 


