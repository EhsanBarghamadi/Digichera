import pytest

from django.urls import reverse
from pytest_django.asserts import assertRedirects
from product.tests.factories import ProductFactory
from cart.models import Cart


@pytest.fixture
def valid_registration_data():
    return {
        "phone": "09123456789",
        "password": "StrongPassword!",
        "confirm_password": "StrongPassword!",
        "first_name": "John",
        "last_name": "Doe",
        "role": "customer",
    }


@pytest.fixture()
def guest_cart_with_product(client):
    product = ProductFactory()
    cart_add_url = reverse("cart:add", args=[product.id])
    data = {"quantity": 5}

    response = client.post(cart_add_url, data=data)

    assertRedirects(response, reverse("cart:detail"), fetch_redirect_response=False)
    session_key = client.session.session_key
    assert Cart.objects.filter(session_key=session_key, user=None).count() == 1
    cart = Cart.objects.get(session_key=session_key, user=None)
    assert cart.items.filter(product=product).count() == 1
    user_item = cart.items.get(product=product)
    assert user_item.quantity == data["quantity"]

    return product, session_key, data["quantity"]
