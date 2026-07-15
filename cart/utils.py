from .models import Cart, CartItem

def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart
    
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    cart, _ = Cart.objects.get_or_create(session_key=session_key, user=None)
    return cart

def merge_guest_cart_into_user_cart(session_key, user):
    if not session_key:
        return

    try:
        guest_cart = Cart.objects.get(session_key=session_key, user=None)
    except Cart.DoesNotExist:
        return

    user_cart, _ = Cart.objects.get_or_create(user=user)

    for item in guest_cart.items.all():
        user_item, created = CartItem.objects.get_or_create(
            cart = user_cart,
            product = item.product,
            defaults = {'quantity': item.quantity}
        )
        if not created:
            user_item.quantity += item.quantity
            user_item.save()
    
    guest_cart.delete()