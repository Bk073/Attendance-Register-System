import pytest
from django.conf import settings

from django.core.exceptions import ValidationError

from ..models import validate_number
from ..tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_user_get_absolute_url(user: settings.AUTH_USER_MODEL):
    assert user.get_absolute_url() == f"/users/{user.username}/"

def test_validate_number():
    with pytest.raises(ValidationError) as e:
        validate_number(1)
    assert "1 not correct format" in str(e.value)

@pytest.fixture
def valid_user():
    return UserFactory(address="hello")


def test_user_is_created_with_password_by_userfactory(valid_user):
    assert valid_user.password