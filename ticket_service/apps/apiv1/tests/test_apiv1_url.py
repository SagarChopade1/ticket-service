from django.urls import reverse

def test_swagger_url():
    url = reverse("swagger-ui")
    assert url == '/api/v1/swagger/'

def test_redoc_url():
    url = reverse("schema-redoc")
    assert url == '/api/v1/redoc/'