from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .froms import ProductForm
from .models import Product, ProductImage, Category

def product_list(request):
    products = Product.objects.all(is_active=True)
    categories = Category.objects.all(is_active=True)
    return render(request, 'product/product_list.html', {'products': products, 'categories': categories})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, 'product/product_detail.html', {'product': product,})

@login_required
def product_create(request):
    user = request.user
    if not hasattr(user, 'store'):
        messages.error(request, 'برای افزودن محصول ابتدا باید یک فروشگاه بسازید.')
        return redirect('store:create')
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
            return redirect('account:profile')
    else:
        form = ProductForm()
    return render(request, 'product/product_form.html', {'form': form})

@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if not hasattr(request.user, 'store') or product.store != request.user.store:
        messages.error(request, 'شما اجازه‌ی ویرایش این محصول را ندارید.')
        return redirect('account:profile')
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
            return redirect('account:profile')
    else:
        form = ProductForm(instance=product)
    return render(request, 'product/product_form.html', {'form': form})

