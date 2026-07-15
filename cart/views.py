from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from product.models import Product
from .models import CartItem
from .utils import get_or_create_cart


def cart_detail(request):
    cart = get_or_create_cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart = get_or_create_cart(request)
    quantity = int(request.POST.get('quantity', 1))
    next_page = request.POST.get('next') or request.GET.get('next')

    existing_item = CartItem.objects.filter(cart=cart, product=product).first()
    current_quantity = existing_item.quantity if existing_item else 0
    new_quantity = current_quantity + quantity

    if new_quantity > product.stock:
        messages.warning(request, 'درخواست شما بیشتر از موجودی انبار است!')
        return redirect(next_page or 'cart:detail')
    
    if existing_item:
        existing_item.quantity = new_quantity
        existing_item.save()
    else:
        CartItem.objects.create(cart=cart, product=product, quantity=new_quantity)

    messages.success(request, f'{product.name} ✖ { quantity } به سبد خرید اضافه کن.')
    return redirect(next_page or 'cart:detail')


def cart_update(request, item_id):
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    quantity = int(request.POST.get('quantity', 1))

    if quantity <= 0:
        item.delete()
        messages.info(request, 'محصول از سبد خرید حذف شد')

    else:
        item.quantity = quantity
        item.save()
        messages.success(request, 'تعداد بروزرسانی شد')
    return redirect('cart:detail')

def cart_remove(request, item_id):
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()
    messages.info(request, 'محصول از سبد خرید حذف شد')
    return redirect('cart:detail')