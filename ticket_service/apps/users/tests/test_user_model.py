import pytest
from users.models import User
from django.db.utils import IntegrityError


@pytest.mark.django_db
def test_user_model_with_all_field():
    user = User.objects.create_user(
        email="test@gmail.com", first_name="test", last_name="testing"
    )
    user.set_password("test")
    assert user.email == "test@gmail.com"
    assert user.first_name == "test"
    assert user.last_name == "testing"
    assert user.is_active == True
    assert user.is_staff == False
    assert user.password is not None


@pytest.mark.django_db
def test_user_model_with_duplicate_email():
    user = User.objects.create_user(
        email="test@gmail.com", first_name="test", last_name="testing"
    )
    user.set_password("test")
    with pytest.raises(IntegrityError) as e:
        User.objects.create_user(
            email="test@gmail.com", first_name="test", last_name="testing"
        )
    assert e.value is not None
    assert user.email == "test@gmail.com"
    assert user.first_name == "test"
    assert user.last_name == "testing"
    assert user.is_active == True
    assert user.is_staff == False
    assert user.password is not None


@pytest.mark.django_db
def test_user_model_without_last_name():
    user = User.objects.create_user(email="test@gmail.com", first_name="test")
    user.set_password("test")
    assert user.email == "test@gmail.com"
    assert user.first_name == "test"
    assert user.last_name == ""
    assert user.is_active == True
    assert user.is_staff == False
    assert user.password is not None


@pytest.mark.django_db
def test_user_model_without_email():
    with pytest.raises(ValueError) as ve:
        user = User.objects.create_user(
            email="", first_name="test", last_name="testing"
        )
    assert str(ve.value) == "Users must have an email address"
