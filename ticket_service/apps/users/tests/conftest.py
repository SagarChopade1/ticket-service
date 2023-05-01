import pytest
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from users.models import User
from oauth2_provider.models import Application
import json


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user():
    data = {
        "first_name": "test",
        "last_name": "test",
        "email": "test@gmail.com",
        "password": "test",
    }
    user = User.objects.create_user(**data)
    user.set_password("test")
    user.save()
    return user


@pytest.fixture
def app(user):
    app = Application(
        client_type=Application.CLIENT_PUBLIC,
        authorization_grant_type=Application.GRANT_PASSWORD,
        redirect_uris="https://www.none.com/oauth2/callback",
        name="dummy",
        user=user,
    )
    app.save()
    return {"client_id": app.client_id, "client_secret": app.client_secret}


@pytest.fixture
def auth_client(client, app):
    url = reverse("token")
    client_id = app["client_id"]
    client_secret = app["client_secret"]
    data = {
        "username": "test@gmail.com",
        "password": "test",
        "client_id": client_id,
        "client_secrete": client_secret,
        "grant_type": "password",
    }
    response = client.post(url, data=data)
    token = json.loads(response.content)["access_token"]
    client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    return client


@pytest.fixture
def user_profile_url():
    return reverse("me")


