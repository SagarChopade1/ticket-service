import pytest
from rest_framework.reverse import reverse
import json
from django.conf import settings
from rest_framework import status


@pytest.mark.django_db
def test_journey_master_listing_without_authentication(client, user_profile_url):
    response = client.get(user_profile_url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_user_profile_api(auth_client, user_profile_url):
    response = auth_client.get(user_profile_url)
    actual_response = json.loads(response.content)
    expected_response = {
        "email": "test@gmail.com",
        "first_name": "test",
        "last_name": "test",
        "role":"PERSONNEL"
    }
    assert expected_response == actual_response
