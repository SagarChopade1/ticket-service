import pytest
from users.models import User


@pytest.mark.django_db
def test_manager_create_user():
    userdata = User.objects.create_user(email="test@gmail.com", password="test")
    assert userdata.email == "test@gmail.com"
    assert userdata.password is not None
    assert userdata.is_staff == False
    assert userdata.is_superuser == False
    assert userdata.is_active == True


@pytest.mark.django_db
def test_manager_create_superuser():
    userdata = User.objects.create_superuser(email="test@gmail.com", password="test")
    assert userdata.email == "test@gmail.com"
    assert userdata.password is not None
    assert userdata.is_staff == True
    assert userdata.is_superuser == True
    assert userdata.is_active == True


@pytest.mark.django_db
def test_manage_create_user_without_password():
    userdata = User.objects.create_user(email="test@gmail.com")
    assert userdata.email == "test@gmail.com"
    assert userdata.password is not None
    assert userdata.is_staff == False
    assert userdata.is_superuser == False
    assert userdata.is_active == True


@pytest.mark.django_db
def test_manager_create_superuser_without_password():
    userdata = User.objects.create_superuser(email="test@gmail.com")
    assert userdata.email == "test@gmail.com"
    assert userdata.password is not None
    assert userdata.is_staff == True
    assert userdata.is_superuser == True
    assert userdata.is_active == True


@pytest.mark.django_db
def test_user_manager_create_superuser_with_is_staff():
    with pytest.raises(ValueError) as ve:
        User.objects.create_superuser(email="test@gmail.com", is_staff=False)
    assert str(ve.value) == "Superuser must have is_staff=True."


@pytest.mark.django_db
def test_user_manager_create_superuser_with_is_admin():
    with pytest.raises(ValueError) as ve:
        User.objects.create_superuser(email="test@gmail.com", is_superuser=False)
    assert str(ve.value) == "Superuser must have is_superuser=True."
