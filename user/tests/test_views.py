import pytest

from django.urls import reverse
from django.contrib.messages import get_messages
from http import HTTPStatus
from user.models import CustomUser
from user.forms import CustomUserCreateForm
from user.tests.factories import CustomUserFactory
from pytest_django.asserts import assertTemplateUsed, assertRedirects


def test_register_view_get_renders_registration_page(client):
    register_url = reverse("user:register")

    response = client.get(register_url)

    assert response.status_code == HTTPStatus.OK
    assert "form" in response.context
    assert isinstance(response.context["form"], CustomUserCreateForm)
    assertTemplateUsed(response, "user/register.html")


@pytest.mark.django_db
def test_register_view_successfully_registers_user(client, valid_registration_data):
    register_url = reverse("user:register")

    response = client.post(register_url, data=valid_registration_data)

    assert response.status_code == HTTPStatus.FOUND
    assertRedirects(response, reverse("page:home"))
    user = CustomUser.objects.get(phone=valid_registration_data["phone"])
    assert user.role == valid_registration_data["role"]
    assert user.first_name == valid_registration_data["first_name"]
    assert user.last_name == valid_registration_data["last_name"]
    assert user.password != valid_registration_data["password"]
    assert user.check_password(valid_registration_data["password"])
    assert response.wsgi_request.user.is_authenticated
    assert response.wsgi_request.user.id == user.id
    assert any(
        item.level_tag == "success" for item in get_messages(response.wsgi_request)
    )


@pytest.mark.django_db
def test_register_view_rejects_staff_role(client, valid_registration_data):
    valid_registration_data["role"] = "staff"
    register_url = reverse("user:register")

    response = client.post(register_url, data=valid_registration_data)

    assert response.status_code == HTTPStatus.OK
    with pytest.raises(CustomUser.DoesNotExist):
        CustomUser.objects.get(phone=valid_registration_data["phone"])
    form = response.context["form"]
    assert "role" in form.errors


@pytest.mark.django_db
def test_register_view_rejects_invalid_password_confirmation(
    client, valid_registration_data
):
    valid_registration_data["confirm_password"] = (
        valid_registration_data["password"] + "1234"
    )
    register_url = reverse("user:register")

    response = client.post(register_url, data=valid_registration_data)

    assert response.status_code == HTTPStatus.OK
    with pytest.raises(CustomUser.DoesNotExist):
        CustomUser.objects.get(phone=valid_registration_data["phone"])
    form = response.context["form"]
    assert "__all__" in form.errors


@pytest.mark.django_db
def test_register_view_rejects_duplicate_phone(client, valid_registration_data):
    user = CustomUserFactory()
    valid_registration_data["phone"] = user.phone
    register_url = reverse("user:register")

    response = client.post(register_url, data=valid_registration_data)

    assert response.status_code == HTTPStatus.OK
    assert CustomUser.objects.filter(phone=user.phone).count() == 1
    form = response.context["form"]
    assert "phone" in form.errors


@pytest.mark.parametrize("role", ["customer", "seller"])
@pytest.mark.django_db
def test_register_view_successfully_registers_allowed_roles(
    client, valid_registration_data, role
):
    valid_registration_data["role"] = role
    register_url = reverse("user:register")

    response = client.post(register_url, data=valid_registration_data)

    assert response.status_code == HTTPStatus.FOUND
    user = CustomUser.objects.get(phone=valid_registration_data["phone"])
    assert user.role == role
