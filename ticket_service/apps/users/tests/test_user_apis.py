import pytest
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
import json
from users import constants
from django.conf import settings

client = APIClient()


@pytest.mark.django_db
def test_register_user_with_all_required_details():
    url = reverse("register")
    payload = {
        "email": "sagar@gmail.com",
        "first_name": "Sagar",
        "last_name": "Chopade",
        "password": "Team@1234l",
    }

    response = client.post(url, payload)
    data = response.data
    assert data["email"] == payload["email"]
    assert data["first_name"] == payload["first_name"]
    assert data["last_name"] == payload["last_name"]
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_register_user_without_email():
    url = reverse("register")
    payload = {"first_name": "Sagar", "last_name": "Chopade", "password": "Team@1234l"}

    response = client.post(url, payload)
    data = response.data
    assert data["email"][0] == constants.REQUIRED_MESSAGE
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_register_user_without_password():
    url = reverse("register")
    payload = {
        "email": "sagar@gmail.com",
        "first_name": "Sagar",
        "last_name": "Chopade",
    }

    response = client.post(url, payload)
    data = response.data
    assert data["password"][0] == constants.REQUIRED_MESSAGE
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_login_user_with_correct_credentials(app):
    url = reverse("token")
    payload = {
        "username": "test@gmail.com",
        "password": "test",
        "client_id": app["client_id"],
        "client_secrete": app["client_secret"],
        "grant_type": "password",
    }
    response = client.post(url, data=payload)
    data = json.loads(response.content)
    assert data["access_token"] is not None
    assert data["expires_in"] == settings.OAUTH2_PROVIDER["ACCESS_TOKEN_EXPIRE_SECONDS"]
    assert data["token_type"] == "Bearer"
    assert data["scope"] == "read"
    assert data["refresh_token"] is not None
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_login_user_with_incorrect_credentials(app):
    url = reverse("token")
    payload = {
        "username": "test@gmail.com",
        "password": "wrongpassword",
        "client_id": app["client_id"],
        "client_secrete": app["client_secret"],
        "grant_type": "password",
    }
    response = client.post(url, payload)
    data = json.loads(response.content)
    assert data["error"] == constants.INVALID_GRANT_MESSAGE
    assert data["error_description"] == constants.INVALID_CREDENTIALS_MESSAGE
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_login_user_without_client_id(app):
    url = reverse("token")
    data = {
        "username": "test@gmail.com",
        "password": "test",
        "client_secrete": app["client_secret"],
        "grant_type": "password",
    }
    response = client.post(url, data)
    data = json.loads(response.content)
    assert data["error"] == constants.INVALID_CLIENT_MESSAGE
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_login_user_without_username(app):
    url = reverse("token")
    data = {
        "password": "wrongpassword",
        "client_id": app["client_id"],
        "client_secrete": app["client_secret"],
        "grant_type": "password",
    }
    response = client.post(url, data)
    data = json.loads(response.content)
    assert data["error"] == constants.INVALID_REQUEST_MESSAGE
    assert data["error_description"] == constants.MISSING_USERNAME_MESSAGE
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_login_user_without_password(app):
    url = reverse("token")
    payload = {
        "username": "test@gmail.com",
        "client_id": app["client_id"],
        "client_secrete": app["client_secret"],
        "grant_type": "password",
    }
    response = client.post(url, data=payload)
    data = json.loads(response.content)
    assert data["error"] == constants.INVALID_REQUEST_MESSAGE
    assert data["error_description"] == constants.MISSING_PASSWORD_MESSAGE
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_login_user_without_grant_type(app):
    url = reverse("token")
    payload = {
        "username": "test@gmail.com",
        "password": "test",
        "client_id": app["client_id"],
        "client_secrete": app["client_secret"],
    }
    response = client.post(url, data=payload)
    data = json.loads(response.content)
    assert data["error"] == constants.INVALID_GRANT_TYPE_MESSAGE
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_logout_user(client, app):
    loginurl = reverse("token")
    payload = {
        "username": "test@gmail.com",
        "password": "test",
        "client_id": app["client_id"],
        "client_secrete": app["client_secret"],
        "grant_type": "password",
    }
    response = client.post(loginurl, data=payload)
    token = json.loads(response.content)["access_token"]
    url = reverse("revoke_token")
    payload = {
        "client_id": app["client_id"],
        "client_secrete": app["client_secret"],
        "token": token,
    }
    response = client.post(url, payload)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_logout_user_without_token(client, app):
    loginurl = reverse("token")
    payload = {
        "username": "test@gmail.com",
        "password": "test",
        "client_id": app["client_id"],
        "client_secrete": app["client_secret"],
        "grant_type": "password",
    }
    response = client.post(loginurl, data=payload)
    token = json.loads(response.content)["access_token"]
    url = reverse("revoke_token")
    payload = {
        "client_id": app["client_id"],
        "client_secrete": app["client_secret"],
    }
    response = client.post(url, payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_should_create_user_with_valid_details(auth_client):
    url = reverse("register")
    payload = {
        "first_name": "test",
        "last_name": "user",
        "email": "testuser@gmail.com",
        "password": "test",
    }
    response = auth_client.post(url, payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == {
        "email": "testuser@gmail.com",
        "first_name": "test",
        "last_name": "user",
        "role":"PERSONNEL"

    }


@pytest.mark.django_db
def test_should_fail_create_user_with_already_exist_email_id(auth_client, user):
    url = reverse("register")
    payload = {
        "first_name": "test",
        "last_name": "test",
        "email": "test@gmail.com",
        "password": "test",
    }
    response = auth_client.post(url, payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["email"][0] == constants.EMAIL_EXISTS


@pytest.mark.django_db
def test_should_update_user_with_valid_details(auth_client, user):
    url = reverse("me")
    payload = {"first_name": "Testing"}
    response = auth_client.patch(url, payload)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        "email": "test@gmail.com",
        "first_name": "Testing",
        "last_name": "test",
    }
