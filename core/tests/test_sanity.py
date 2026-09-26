import pytest
from user.models import CustomUser

@pytest.mark.django_db
def test_database_is_accessible():
    assert CustomUser.objects.count() == 0