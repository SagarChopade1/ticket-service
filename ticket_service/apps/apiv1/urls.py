from django.urls import path, include
from ticket_service.config.settings import django

from django.views.generic import TemplateView


urlpatterns = [
    path("users/", include("users.api.urls"), name="users_api"),
]

if django.DEBUG:
    urlpatterns += [
        path(
            "redoc/",
            TemplateView.as_view(
                template_name="apiv1/redoc.html",
                extra_context={
                    "schema_url": "openapi-schema",
                    "host": django.SWAGGER_HOST_NAME,
                },
            ),
            name="schema-redoc",
        ),
        path(
            "swagger/",
            TemplateView.as_view(
                template_name="apiv1/swagger.html",
                extra_context={
                    "schema_url": "openapi-schema",
                    "host": django.SWAGGER_HOST_NAME,
                },
            ),
            name="swagger-ui",
        ),
    ]
