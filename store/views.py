from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from user.models import CustomUser
from core.decorators import store_required
from .forms import StoreForm

@login_required
@store_required()
def store_detail(request):
    return render(request, 'store/store_detail.html')


@login_required
@store_required()
def store_update(request):
    store = request.user.store
    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES, instance=store)
        if form.is_valid():
            form.save()
            messages.success(request, f'فروشگاه شما با موفقیت بروزرسانی شد')
            return redirect('store:detail')
    else:
        form = StoreForm(instance=store)
    return render(request, 'store/store_form.html', {'form': form})


@login_required
def store_create(request):
    user = request.user
    if user.role == CustomUser.Roles.CUSTOMER or user.role == CustomUser.Roles.STAFF:
        messages.error(request, 'شما دسترسی برای ساخت فروشگاه ندارید')
        return redirect('page:home')
    if hasattr(user, 'store'):
        messages.info(request, 'شما از قبل یک فروشگاه دارید')
        return redirect('account:detail')
    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                store = form.save(commit=False)
                store.owner = request.user
                store.save()
                messages.success(request, 'تبریک! فروشگاه شما با موفقیت ایجاد شد.')
                return redirect('account:detail')
            except Exception as e:
                messages.error(request, 'خطایی رخ داد: ' + str(e))
    else:
        form = StoreForm()
    return render(request, 'store/store_form.html', {'form': form})
