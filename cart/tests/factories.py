import factory

from cart.models import Cart, CartItem


class CartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cart

    session_key = None
    user = None

    class Params:
        with_user = factory.Trait(
            user=factory.SubFactory("user.tests.factories.CustomUserFactory"),
            session_key=None,
        )


class CartItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CartItem

    cart = factory.SubFactory("cart.tests.factories.CartFactory")
    product = factory.SubFactory("product.tests.factories.ProductFactory")
    quantity = 1
