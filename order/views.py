from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import connection

from cart.utils import get_or_create_cart
from product.models import Product
from .models import Order, OrderItem


@login_required
@transaction.atomic
def checkout(request):
    if request.method != 'POST':
        return redirect('cart:detail')
    cart = get_or_create_cart(request)
    items = cart.items.select_related('product', 'product__store').all()

    if not items:
        messages.info(request, 'سبد خرید شما خالی است')
        return redirect('cart:detail')
    
    if not hasattr(request.user, 'profile') or not request.user.profile.location or not request.user.profile.postal_code:
        messages.info(request, 'لطفا ابتدا اطلاعات پروفایل خود را تکمیل کنید')
        return redirect('account:update')

    items_by_store = {}
    for item in items:
        store = item.product.store
        items_by_store.setdefault(store, []).append(item)

    for item in items:
        if connection.vendor != 'sqlite':
            product = Product.objects.select_for_update().get(pk=item.product.pk)
        else:
            product = Product.objects.get(pk=item.product.pk)
        if item.quantity > product.stock:
            messages.error(request, f"موجودی {product.name} کافی نیست")
            return redirect('cart:detail')
        
    created_order_ids = []
    profile = request.user.profile
    for store, store_items in items_by_store.items():
        order = Order.objects.create(
            user=request.user,
            store=store,
            status=Order.Status.PENDING,
            shipping_address=f"{profile.location} | کد پستی : {profile.postal_code}"
        )
        for item in store_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                price=item.product.price,
                quantity=item.quantity
            )
            item.product.stock -= item.quantity
            item.product.save()
        created_order_ids.append(order.pk)
    cart.items.all().delete()

    request.session['last_order_ids'] = created_order_ids
    messages.success(request, "سفارش شما با موققیت ثبت شد")
    return redirect('page:bank')


@login_required
def order_success(request):
    order_ids = request.session.pop('last_order_ids', None)
    if not order_ids:
        return redirect('cart:detail')
    
    with transaction.atomic():
        created_orders = Order.objects.filter(pk__in=order_ids, user=request.user).prefetch_related('items')
        for order in created_orders:
            order.status = Order.Status.PAID
            order.save()

    created_orders = Order.objects.filter(pk__in=order_ids, user=request.user).prefetch_related('items')
    return render(request, 'order/order_detail.html', {'created_orders': created_orders})
    

