import pytest

from account.models import Profile
from user.tests.factories import CustomUserFactory


@pytest.mark.django_db
def test_create_user_creates_profile():
    user = CustomUserFactory()

    assert Profile.objects.filter(user=user).exists()


@pytest.mark.django_db
def test_saving_existing_user_does_not_create_duplicate_profile():
    user = CustomUserFactory()

    assert Profile.objects.filter(user=user).exists()
    
    user.save()

    assert Profile.objects.filter(user=user).count() == 1
