import pytest

from django.urls import reverse
from django.contrib.messages import get_messages
from http import HTTPStatus
from user.models import CustomUser
from user.forms import CustomUserCreateForm
from user.tests.factories import CustomUserFactory
from cart.models import Cart
from product.tests.factories import ProductFactory
from pytest_django.asserts import assertTemplateUsed, assertRedirects

pytestmark = pytest.mark.django_db


def test_register_view_get_renders_registration_page(client):
    register_url = reverse("user:register")

    response = client.get(register_url)

    assert response.status_code == HTTPStatus.OK
    assert "form" in response.context
    assert isinstance(response.context["form"], CustomUserCreateForm)
    assertTemplateUsed(response, "user/register.html")


def test_register_view_successfully_registers_user(client, valid_registration_data):
    register_url = reverse("user:register")

    response = client.post(register_url, data=valid_registration_data)

    assertRedirects(response, reverse("page:home"), fetch_redirect_response=False)
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


def test_register_view_rejects_staff_role(client, valid_registration_data):
    valid_registration_data["role"] = "staff"
    register_url = reverse("user:register")

    response = client.post(register_url, data=valid_registration_data)

    assert response.status_code == HTTPStatus.OK
    assert not CustomUser.objects.filter(
        phone=valid_registration_data["phone"]
    ).exists()
    form = response.context["form"]
    assert "role" in form.errors


def test_register_view_rejects_invalid_password_confirmation(
    client, valid_registration_data
):
    valid_registration_data["confirm_password"] = (
        valid_registration_data["password"] + "1234"
    )
    register_url = reverse("user:register")

    response = client.post(register_url, data=valid_registration_data)

    assert response.status_code == HTTPStatus.OK
    assert not CustomUser.objects.filter(
        phone=valid_registration_data["phone"]
    ).exists()
    form = response.context["form"]
    assert "__all__" in form.errors


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
def test_register_view_successfully_registers_allowed_roles(
    client, valid_registration_data, role
):
    valid_registration_data["role"] = role
    register_url = reverse("user:register")

    response = client.post(register_url, data=valid_registration_data)

    assert response.status_code == HTTPStatus.FOUND
    user = CustomUser.objects.get(phone=valid_registration_data["phone"])
    assert user.role == role


def test_register_view_merges_guest_cart_after_registration(
    client, valid_registration_data
):
    product = ProductFactory()

    cart_add_url = reverse("cart:add", args=[product.id])
    data = {"quantity": 5}

    response_1 = client.post(cart_add_url, data=data)

    session_key_guest = client.session.session_key
    assert Cart.objects.filter(session_key=session_key_guest, user=None).exists()
    assertRedirects(response_1, reverse("cart:detail"), fetch_redirect_response=False)

    register_url = reverse("user:register")

    response_2 = client.post(register_url, data=valid_registration_data)

    assert not Cart.objects.filter(session_key=session_key_guest, user=None).exists()
    cart_user = Cart.objects.get(user=response_2.wsgi_request.user)
    assert cart_user.items.filter(product=product).count() == 1
    assert cart_user.items.count() == 1
    user_item = cart_user.items.get(product=product)
    assert user_item.quantity == data["quantity"]
    assertRedirects(response_2, reverse("page:home"), fetch_redirect_response=False)
