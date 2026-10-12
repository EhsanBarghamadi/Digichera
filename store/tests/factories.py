import factory

from store.models import Store


class StoreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Store

    owner = factory.SubFactory("user.tests.factories.CustomUserFactory", seller=True)
    store_name = factory.Sequence(lambda n: f"store_name_{n}")
    store_phone = factory.Sequence(lambda n: f"0{9000000000 + n}")
    is_active = factory.Faker("boolean")
