from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from core.decorators import store_required, store_owner_required
from .forms import ProductForm
from .models import Product, ProductImage, Category


def product_list(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.filter(is_active=True)
    return render(request, 'product/product_list.html', {'products': products, 'categories': categories})


def product_category(request, category_id):
    products = Product.objects.filter(is_active=True, category=category_id)
    categories = Category.objects.filter(is_active=True)
    return render(request, 'product/product_list.html', {'products': products, 'categories':categories})


def product_search(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.filter(is_active=True)
    query = request.GET.get('q', '')

    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(store__store_name__icontains=query) |
            Q(description__icontains=query)
        )
    return render(request, 'product/product_list.html', {'products': products, 'categories':categories})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, 'product/product_detail.html', {'product': product,})


@login_required
@store_required
def product_create(request):
    user = request.user
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.store = user.store
            product.save()
            files = request.FILES.getlist('image')
            for f in files:
                ProductImage.objects.create(product=product, title=product.name, image=f)
            messages.success(request,'محصول شما با موفقیت ایجاد شد')
            return redirect('account:detail')
    else:
        form = ProductForm()
    return render(request, 'product/product_form.html', {'form': form})


@login_required
@store_owner_required(Product)
def product_update(request, pk):
    product = request.obj
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            new_images = request.FILES.getlist('image')
            if new_images:
                product.images.all().delete()
            for img in new_images:
                    ProductImage.objects.create(product=product, image=img)
            messages.success(request, f'محصول {product.name} با موفقیت بروزرسانی شد.')
            return redirect('account:detail')
    else:
        form = ProductForm(instance=product)
    return render(request, 'product/product_form.html', {'form': form})


