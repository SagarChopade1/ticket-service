# Generated by Django 4.1.5 on 2023-05-01 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                (
                    "email",
                    models.EmailField(
                        max_length=254, unique=True, verbose_name="email address"
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=100, verbose_name="First Name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=100, verbose_name="Last Name"
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=False, help_text="Active user", verbose_name="active"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("ADMIN", "Admin"),
                            ("MANAGER", "Manager"),
                            ("PERSONNEL", "Personnel"),
                        ],
                        default="PERSONNEL",
                        max_length=20,
                        verbose_name="Role",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "users",
                "ordering": ["-created_at", "email"],
            },
        ),
        migrations.AddIndex(
            model_name="user",
            index=models.Index(fields=["email"], name="users_user_email_6f2530_idx"),
        ),
    ]
