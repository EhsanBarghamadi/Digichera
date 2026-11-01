import pytest

from django.urls import reverse
from django.contrib.messages import get_messages
from http import HTTPStatus
from user.models import CustomUser
from user.forms import CustomUserCreateForm, CustomUserLoginForm
from user.tests.factories import CustomUserFactory
from cart.models import Cart
from cart.tests.factories import CartFactory, CartItemFactory
from product.tests.factories import ProductFactory
from pytest_django.asserts import assertTemplateUsed, assertRedirects

pytestmark = pytest.mark.django_db

PASSWORD = "StrongPassword!123"


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


def test_login_view_get(client):
    login_url = reverse("user:login")

    response = client.get(login_url)

    assert response.status_code == HTTPStatus.OK
    assert "form" in response.context
    assert isinstance(response.context["form"], CustomUserLoginForm)
    assertTemplateUsed(response, "user/login.html")


def test_login_view_success(client):
    user = CustomUserFactory(password=PASSWORD)

    login_url = reverse("user:login")

    data = {"phone": user.phone, "password": PASSWORD}
    response = client.post(login_url, data=data)

    assertRedirects(response, reverse("page:home"), fetch_redirect_response=False)
    assert response.wsgi_request.user.is_authenticated
    assert response.wsgi_request.user.id == user.id
    assert any(
        item.level_tag == "success" for item in get_messages(response.wsgi_request)
    )


@pytest.mark.parametrize(
    "phone, user_exists",
    [
        ("09123456789", True),
        ("09123456789", False),
    ],
)
def test_login_view_rejects_invalid_credentials(client, phone, user_exists):
    if user_exists:
        CustomUserFactory(phone=phone, password=PASSWORD)

    login_url = reverse("user:login")

    data = {
        "phone": phone,
        "password": "WrongPassword",
    }
    response = client.post(login_url, data=data)

    assert response.status_code == HTTPStatus.OK
    assert not response.wsgi_request.user.is_authenticated
    form = response.context["form"]
    assert "phone" in form.errors
    assert form.errors["phone"] == ["شماره موبایل یا رمز عبور اشتباه است."]


def test_login_view_inactive_user(client):
    user = CustomUserFactory(is_active=False, password=PASSWORD)

    login_url = reverse("user:login")

    data = {
        "phone": user.phone,
        "password": PASSWORD,
    }
    response = client.post(login_url, data=data)

    assert response.status_code == HTTPStatus.OK
    assert not response.wsgi_request.user.is_authenticated
    form = response.context["form"]
    assert "phone" in form.errors
    assert form.errors["phone"] == ["شماره موبایل یا رمز عبور اشتباه است."]


@pytest.mark.parametrize(
    "missing_field",
    [
        "phone",
        "password",
    ],
)
def test_login_view_rejects_missing_credentials(client, missing_field):
    login_url = reverse("user:login")

    if missing_field == "phone":
        data = {
            "phone": "",
            "password": PASSWORD,
        }
    elif missing_field == "password":
        user = CustomUserFactory()
        data = {
            "phone": user.phone,
            "password": "",
        }

    response = client.post(login_url, data=data)

    assert response.status_code == HTTPStatus.OK
    assert not response.wsgi_request.user.is_authenticated
    form = response.context["form"]
    assert missing_field in form.errors


def test_login_view_merges_guest_cart(client):
    product = ProductFactory()

    cart_add_url = reverse("cart:add", args=[product.id])
    data = {"quantity": 5}

    response_1 = client.post(cart_add_url, data=data)

    assertRedirects(response_1, reverse("cart:detail"), fetch_redirect_response=False)
    session_key_guest = client.session.session_key
    assert Cart.objects.filter(session_key=session_key_guest, user=None).exists()

    login_url = reverse("user:login")

    user = CustomUserFactory(password=PASSWORD)

    response_2 = client.post(
        login_url, data={"phone": user.phone, "password": PASSWORD}
    )

    assert response_2.wsgi_request.user.is_authenticated
    assert not Cart.objects.filter(session_key=session_key_guest, user=None).exists()
    cart_user = Cart.objects.get(user=response_2.wsgi_request.user)
    assert cart_user.items.filter(product=product).count() == 1
    assert cart_user.items.count() == 1
    user_item = cart_user.items.get(product=product)
    assert user_item.quantity == data["quantity"]
    assertRedirects(response_2, reverse("page:home"), fetch_redirect_response=False)


def test_login_view_merges_duplicate_cart_items(client):
    product = ProductFactory()

    cart_add_url = reverse("cart:add", args=[product.id])
    data = {"quantity": 3}

    response_1 = client.post(cart_add_url, data=data)

    assertRedirects(response_1, reverse("cart:detail"), fetch_redirect_response=False)
    session_key_guest = client.session.session_key
    assert Cart.objects.filter(session_key=session_key_guest, user=None).exists()

    login_url = reverse("user:login")

    user = CustomUserFactory(password=PASSWORD)
    cart = CartFactory(user=user)
    cart_item = CartItemFactory(cart=cart, product=product, quantity=2)

    response_2 = client.post(
        login_url, data={"phone": user.phone, "password": PASSWORD}
    )

    assert response_2.wsgi_request.user.is_authenticated
    assert not Cart.objects.filter(session_key=session_key_guest, user=None).exists()
    cart_user = Cart.objects.get(user=response_2.wsgi_request.user)
    assert cart_user.items.filter(product=product).count() == 1
    assert cart_user.items.count() == 1
    user_item = cart_user.items.get(product=product)
    assert user_item.quantity == (data["quantity"] + cart_item.quantity)
    assertRedirects(response_2, reverse("page:home"), fetch_redirect_response=False)


def test_login_view_without_guest_cart(client):
    login_url = reverse("user:login")

    assert client.session.session_key is not None 
    assert not Cart.objects.filter(session_key=client.session.session_key, user=None).exists()

    user = CustomUserFactory(password=PASSWORD)
    
    response = client.post(
        login_url, data={"phone": user.phone, "password": PASSWORD}
    )

    assert response.wsgi_request.user.is_authenticated
    assertRedirects(response, reverse("page:home"), fetch_redirect_response=False)
    assert not Cart.objects.filter(session_key=client.session.session_key, user=None).exists()
