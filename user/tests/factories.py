import factory

from user.models import CustomUser


class CustomUserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = CustomUser

    class Params:
        customer = factory.Trait(role=CustomUser.Roles.CUSTOMER)
        seller = factory.Trait(role=CustomUser.Roles.SELLER)
        staff = factory.Trait(role=CustomUser.Roles.STAFF)

    phone = factory.Sequence(lambda n: f"0{9000000000 + n}")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    role = CustomUser.Roles.CUSTOMER
    password = "testpass123"

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)
