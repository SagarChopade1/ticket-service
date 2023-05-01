from django.urls import include, re_path
import oauth2_provider.views as oauth2_views
from users.api import views


urlpatterns = [
    re_path(r"^login/$", oauth2_views.TokenView.as_view(), name="token"),
    re_path(r"^logout/$", oauth2_views.RevokeTokenView.as_view(), name="revoke_token"),
    re_path(r"^register/", views.RegistrationView.as_view(), name="register"),
    re_path(r"^me/", views.UserView.as_view(), name="me"),
]
