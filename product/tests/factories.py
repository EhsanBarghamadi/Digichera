import factory

from product.models import Category, Product


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"category-{n}")
    is_active = True


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    store = factory.SubFactory("store.tests.factories.StoreFactory")
    category = factory.SubFactory("product.tests.factories.CategoryFactory")
    name = factory.Sequence(lambda n: f"product-{n}")
    description = factory.Faker("sentence")
    price = factory.Faker("random_int", min=10, max=5000)
    stock = 10
    is_active = True
