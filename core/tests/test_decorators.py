import pytest

from core.decorators import store_required
from user.tests.factories import CustomUserFactory
from store.tests.factories import StoreFactory
from django.contrib import messages
from django.urls import reverse

view_called = []


@store_required("test_message")
def dummy_view(request):
    view_called.append(True)


@pytest.mark.django_db
def test_store_required_without_store(authenticated_request_factory):
    user = CustomUserFactory()
    request = authenticated_request_factory(user)

    view_called.clear()
    response = dummy_view(request)

    message_list = list(messages.get_messages(request))

    assert response.status_code == 302
    assert response.url == reverse('store:create')
    assert len(message_list) == 1
    assert message_list[0].message == "test_message"
    assert message_list[0].level == messages.ERROR


@pytest.mark.django_db
def test_store_required_with_store(authenticated_request_factory):
    user = CustomUserFactory()
    store = StoreFactory(owner=user)
    request = authenticated_request_factory(user)
    view_called.clear()
    response = dummy_view(request)

    message_list = list(messages.get_messages(request))

    assert response is None
    assert message_list == []
    assert view_called == [True]
