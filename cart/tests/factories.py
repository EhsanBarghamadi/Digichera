import factory

from cart.models import Cart, CartItem


class CartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cart

    session_key = None
    user = None


class CartItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CartItem

    cart = factory.SubFactory("cart.tests.factories.CartFactory")
    product = factory.SubFactory("product.tests.factories.ProductFactory")
    quantity = 1
