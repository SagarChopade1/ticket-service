from django.utils.translation import gettext_lazy as _
from django.db.models import TextChoices


class UserRoleType(TextChoices):
    ADMIN = "ADMIN", "Admin"
    MANAGER = "MANAGER", "Manager"
    PERSONNEL = "PERSONNEL", "Personnel"


EMAIL_EXISTS = _("A user with this email already exists.")
REQUIRED_MESSAGE = _("This field is required.")
INVALID_CLIENT_MESSAGE = _("invalid_client")
INVALID_GRANT_MESSAGE = _("invalid_grant")
INVALID_CREDENTIALS_MESSAGE = _("Invalid credentials given.")
INVALID_REQUEST_MESSAGE = _("invalid_request")
MISSING_USERNAME_MESSAGE = _("Request is missing username parameter.")
MISSING_PASSWORD_MESSAGE = _("Request is missing password parameter.")
INVALID_GRANT_TYPE_MESSAGE = _("unsupported_grant_type")
