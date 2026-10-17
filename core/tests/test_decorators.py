import pytest

from core.decorators import store_required, store_owner_required
from user.tests.factories import CustomUserFactory
from store.tests.factories import StoreFactory
from product.tests.factories import ProductFactory
from product.models import Product
from django.contrib import messages
from django.urls import reverse
from django.http import Http404

view_called = []


@store_required("test_message")
def store_required_view(request):
    view_called.append(True)


@store_owner_required(Product)
def store_owner_required_view(request, pk):
    view_called.append(True)


@store_owner_required(
    Product,
    lookup_field="name",
    lookup_url_kwarg="product_name",
)
def store_owner_required_custom_lookup_view(request, product_name):
    view_called.append(True)


@pytest.mark.django_db
def test_store_required_without_store(authenticated_request_factory):
    user = CustomUserFactory()
    request = authenticated_request_factory(user)

    view_called.clear()
    response = store_required_view(request)

    message_list = list(messages.get_messages(request))

    assert response.status_code == 302
    assert response.url == reverse("store:create")
    assert view_called == []
    assert len(message_list) == 1
    assert message_list[0].message == "test_message"
    assert message_list[0].level == messages.ERROR


@pytest.mark.django_db
def test_store_required_with_store(authenticated_request_factory):
    user = CustomUserFactory()
    store = StoreFactory(owner=user)
    request = authenticated_request_factory(user)
    view_called.clear()
    response = store_required_view(request)

    message_list = list(messages.get_messages(request))

    assert response is None
    assert message_list == []
    assert view_called == [True]


@pytest.mark.django_db
def test_store_owner_required_with_owner(authenticated_request_factory):
    user = CustomUserFactory()
    store = StoreFactory(owner=user)
    product = ProductFactory(store=store)
    request = authenticated_request_factory(user)
    view_called.clear()

    response = store_owner_required_view(request, pk=product.pk)

    message_list = list(messages.get_messages(request))

    assert response is None
    assert message_list == []
    assert view_called == [True]
    assert request.obj == product


@pytest.mark.django_db
def test_store_owner_required_without_owner(authenticated_request_factory):
    user_1 = CustomUserFactory()
    user_2 = CustomUserFactory()
    store = StoreFactory(owner=user_2)
    product = ProductFactory(store=store)

    request = authenticated_request_factory(user_1)
    view_called.clear()

    response = store_owner_required_view(request, pk=product.pk)

    message_list = list(messages.get_messages(request))

    assert response.status_code == 302
    assert response.url == reverse("account:detail")
    assert view_called == []
    assert len(message_list) == 1
    assert message_list[0].message == "شما اجازه‌ی دسترسی به این مورد را ندارید."
    assert message_list[0].level == messages.ERROR


@pytest.mark.django_db
def test_store_owner_required_with_custom_lookup(authenticated_request_factory):
    user = CustomUserFactory()
    store = StoreFactory(owner=user)
    product = ProductFactory(store=store)
    request = authenticated_request_factory(user)
    view_called.clear()

    response = store_owner_required_custom_lookup_view(
        request, product_name=product.name
    )

    message_list = list(messages.get_messages(request))

    assert response is None
    assert message_list == []
    assert view_called == [True]
    assert request.obj == product


@pytest.mark.django_db
def test_store_owner_required_object_not_found(authenticated_request_factory):
    user = CustomUserFactory()
    store = StoreFactory(owner=user)
    product = ProductFactory(store=store)
    request = authenticated_request_factory(user)
    view_called.clear()

    with pytest.raises(Http404):
        store_owner_required_view(request, pk=product.pk + 1)

    assert view_called == []


