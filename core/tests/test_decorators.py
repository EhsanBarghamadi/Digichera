import pytest

from core.decorators import store_required, store_owner_required
from user.tests.factories import CustomUserFactory
from store.tests.factories import StoreFactory
from product.tests.factories import ProductFactory
from product.models import Product
from django.contrib import messages
from django.urls import reverse
from django.http import Http404, HttpResponse


@store_required("test_message")
def store_required_view(request):
    return HttpResponse(content="store_required_view")


@store_owner_required(Product)
def store_owner_required_view(request, pk):
    return HttpResponse(content="store_owner_required_view")


@store_owner_required(
    Product,
    lookup_field="slug",
    lookup_url_kwarg="product_slug",
)
def store_owner_required_custom_lookup_view(request, product_slug):
    return HttpResponse(content="store_owner_required_custom_lookup_view")


@pytest.mark.django_db
def test_store_required_without_store(authenticated_request_factory):
    user = CustomUserFactory()
    request = authenticated_request_factory(user)

    response = store_required_view(request)

    message_list = list(messages.get_messages(request))

    assert response.status_code == 302
    assert response.url == reverse("store:create")
    assert len(message_list) == 1
    assert message_list[0].message == "test_message"
    assert message_list[0].level == messages.ERROR


@pytest.mark.django_db
def test_store_required_with_store(authenticated_request_factory):
    user = CustomUserFactory()
    StoreFactory(owner=user)
    request = authenticated_request_factory(user)
    response = store_required_view(request)

    message_list = list(messages.get_messages(request))

    assert response.status_code == 200
    assert response.content == b"store_required_view"
    assert message_list == []


@pytest.mark.django_db
def test_store_owner_required_with_owner(authenticated_request_factory):
    user = CustomUserFactory()
    store = StoreFactory(owner=user)
    product = ProductFactory(store=store)
    request = authenticated_request_factory(user)

    response = store_owner_required_view(request, pk=product.pk)

    message_list = list(messages.get_messages(request))

    assert response.status_code == 200
    assert response.content == b"store_owner_required_view"
    assert message_list == []
    assert request.obj == product


@pytest.mark.django_db
def test_store_owner_required_without_owner(authenticated_request_factory):
    user_1 = CustomUserFactory()
    user_2 = CustomUserFactory()
    StoreFactory(owner=user_1)
    store = StoreFactory(owner=user_2)
    product = ProductFactory(store=store)

    request = authenticated_request_factory(user_1)

    response = store_owner_required_view(request, pk=product.pk)

    message_list = list(messages.get_messages(request))

    assert response.status_code == 302
    assert response.content == b""
    assert response.url == reverse("account:detail")
    assert len(message_list) == 1
    assert message_list[0].message == "شما اجازه‌ی دسترسی به این مورد را ندارید."
    assert message_list[0].level == messages.ERROR


@pytest.mark.django_db
def test_store_owner_required_without_store(authenticated_request_factory):
    user = CustomUserFactory()
    owner = CustomUserFactory()

    store = StoreFactory(owner=owner)
    product = ProductFactory(store=store)

    request = authenticated_request_factory(user)

    response = store_owner_required_view(request, pk=product.pk)

    message_list = list(messages.get_messages(request))

    assert response.status_code == 302
    assert response.content == b""
    assert response.url == reverse("account:detail")
    assert len(message_list) == 1
    assert message_list[0].message == "شما اجازه‌ی دسترسی به این مورد را ندارید."
    assert message_list[0].level == messages.ERROR


@pytest.mark.django_db
def test_store_owner_required_with_custom_lookup(authenticated_request_factory):
    user = CustomUserFactory()
    store = StoreFactory(owner=user)
    product = ProductFactory(store=store)
    request = authenticated_request_factory(user)

    response = store_owner_required_custom_lookup_view(
        request, product_slug=product.slug
    )

    message_list = list(messages.get_messages(request))

    assert response.status_code == 200
    assert response.content == b"store_owner_required_custom_lookup_view"
    assert message_list == []
    assert request.obj == product


@pytest.mark.django_db
def test_store_owner_required_object_not_found(authenticated_request_factory):
    user = CustomUserFactory()
    store = StoreFactory(owner=user)
    product = ProductFactory(store=store)
    request = authenticated_request_factory(user)

    with pytest.raises(Http404):
        store_owner_required_view(request, pk=-1)
