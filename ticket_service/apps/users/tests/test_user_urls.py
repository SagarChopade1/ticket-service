import pytest
from rest_framework.reverse import reverse
from django.urls import resolve


@pytest.mark.browser
def test_resgister_user_url(client):
    url = reverse("register")
    assert url == "/api/v1/users/register/"
    resolver = resolve("/api/v1/users/register/")
    assert resolver.view_name == "register"


@pytest.mark.browser
def test_me_url():
    url = reverse("me")
    assert url == "/api/v1/users/me/"
    resolver = resolve("/api/v1/users/me/")
    assert resolver.view_name == "me"


@pytest.mark.browser
def test_login_url():
    url = reverse("token")
    assert url == "/api/v1/users/login/"
    resolver = resolve("/api/v1/users/login/")
    assert resolver.view_name == "token"


@pytest.mark.browser
def test_logout_url():
    url = reverse("revoke_token")
    assert url == "/api/v1/users/logout/"
    resolver = resolve("/api/v1/users/logout/")
    assert resolver.view_name == "revoke_token"


