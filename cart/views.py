from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.utils.http import url_has_allowed_host_and_scheme

from product.models import Product
from .models import CartItem
from .utils import get_or_create_cart


def cart_detail(request):
    cart = get_or_create_cart(request)
    return render(request, "cart/cart_detail.html", {"cart": cart})


@require_POST
def cart_add(request, product_id):
    next_url = request.POST.get("next") or request.GET.get("next")
    is_safe_redirect = next_url and url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    )

    if is_safe_redirect or not next_url:
        product = get_object_or_404(Product.objects.visible(), id=product_id)
        cart = get_or_create_cart(request)

        try:
            quantity = int(request.POST.get("quantity", 1))
            if quantity <= 0:
                raise ValueError
        except ValueError:
            messages.warning(request, "درخواست نامعتبر است!")
            return redirect("cart:detail")

        existing_item = CartItem.objects.filter(cart=cart, product=product).first()
        current_quantity = existing_item.quantity if existing_item else 0
        new_quantity = current_quantity + quantity

        if new_quantity > product.stock:
            messages.warning(request, "درخواست شما بیشتر از موجودی انبار است!")
            return redirect(next_url or "cart:detail")

        if existing_item:
            existing_item.quantity = new_quantity
            existing_item.save()
        else:
            CartItem.objects.create(cart=cart, product=product, quantity=new_quantity)

        messages.success(
            request, f"{product.name} ✖ { quantity } به سبد خرید اضافه کن."
        )
        return redirect(next_url or "cart:detail")

    messages.warning(request, "درخواست نامعتبر است!")
    return redirect("cart:detail")


@require_POST
def cart_update(request, item_id):
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    try:
        quantity = int(request.POST.get("quantity", 1))
    except ValueError:
        messages.error(request, "مقدار وارد شده نامعتبر است.")
        return redirect(request.POST.get("next") or "cart:detail")

    if quantity <= 0:
        item.delete()
        messages.info(request, "محصول از سبد خرید حذف شد")

    elif quantity > item.product.stock:
        messages.error(request, "تعداد از موجودی انبار بیشتر است")

    else:
        item.quantity = quantity
        item.save()
        messages.success(request, "تعداد بروزرسانی شد")

    return redirect("cart:detail")


@require_POST
def cart_remove(request, item_id):
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()
    messages.info(request, "محصول از سبد خرید حذف شد")
    return redirect("cart:detail")
