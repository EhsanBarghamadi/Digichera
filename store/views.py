from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

from user.models import CustomUser
from .forms import StoreForm

@login_required
def store_create(request):
    user = request.user
    if user.role == CustomUser.Roles.CUSTOMER or user.role == CustomUser.Roles.STAFF:
        messages.error(request, '⚠️ شما دسترسی برای ساخت فروشگاه ندارید')
        return redirect('page:home')
    if hasattr(user, 'store'):
        messages.info(request, 'شما از قبل یک فروشگاه دارید')
        return redirect('account:profile')
    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                store = form.save(commit=False)
                store.owner = request.user
                store.save()
                messages.success(request, 'تبریک! فروشگاه شما با موفقیت ایجاد شد.')
                return redirect('account:profile')
            except Exception as e:
                messages.error(request, 'خطایی رخ داد: ' + str(e))
    else:
        form = StoreForm()
    return render(request, 'store/store_form.html', {'form': form})
