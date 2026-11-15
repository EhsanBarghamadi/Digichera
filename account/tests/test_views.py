from http import HTTPStatus

import pytest

from django.urls import reverse
from pytest_django.asserts import assertRedirects, assertTemplateUsed, assertContains

from user.tests.factories import CustomUserFactory
from store.tests.factories import StoreFactory

pytestmark = pytest.mark.django_db


def test_profile_detail_redirects_anonymous_user_to_login(client):
    account_url = reverse("account:detail")

    response = client.get(account_url)

    expected_detail_url = f"{reverse('user:login')}?next={account_url}"
    assertRedirects(response, expected_detail_url, fetch_redirect_response=False)


def test_profile_detail_displays_customer_template(client):
    user = CustomUserFactory(customer=True)

    client.force_login(user)

    account_detail_url = reverse("account:detail")

    response = client.get(account_detail_url)

    assert response.status_code == HTTPStatus.OK
    assertTemplateUsed(response, "account/profile_customer_detail.html")


def test_profile_detail_displays_seller_template(client):
    user = CustomUserFactory(seller=True)

    client.force_login(user)

    account_detail_url = reverse("account:detail")

    response = client.get(account_detail_url)

    assert response.status_code == HTTPStatus.OK
    assertTemplateUsed(response, "account/profile_seller_detail.html")


def test_profile_detail_redirects_staff_user_to_admin(client):
    user = CustomUserFactory(staff=True)

    client.force_login(user)

    account_detail_url = reverse("account:detail")

    response = client.get(account_detail_url)

    assertRedirects(response, reverse("admin:index"), fetch_redirect_response=False)


@pytest.mark.parametrize(
    "user_trait",
    ["customer", "seller"],
    ids=["customer", "seller"],
)
def test_profile_detail_displays_address_and_postal_code(client, user_trait):
    user = CustomUserFactory(**{user_trait: True})

    data = {
        "postal_code": "1619614153",
        "location": "تهران، خیابان پاسداران، کوچه شهید یزدانی، پلاک ۱۲، طبقه سوم",
    }
    profile = user.profile
    profile.postal_code = data["postal_code"]
    profile.location = data["location"]
    profile.save()

    client.force_login(user)

    account_detail_url = reverse("account:detail")

    response = client.get(account_detail_url)

    assertContains(response, data["postal_code"])
    assertContains(response, data["location"])


def test_profile_detail_displays_create_store_link_for_seller_without_store(client):
    user = CustomUserFactory(seller=True)

    client.force_login(user)

    account_detail_url = reverse("account:detail")

    response = client.get(account_detail_url)

    assertContains(response, reverse("store:create"))


def test_profile_detail_displays_store_detail_link_for_seller_with_store(client):
    user = CustomUserFactory(seller=True)
    StoreFactory(owner=user)

    client.force_login(user)

    account_detail_url = reverse("account:detail")

    response = client.get(account_detail_url)

    assertContains(response, reverse("store:detail"))
