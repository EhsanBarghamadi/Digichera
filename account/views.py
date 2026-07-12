from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

from user.models import CustomUser
from .models import Profile
from .forms import ProfileForm

@login_required
def profile_view(request):
    user = request.user
    if user.role == CustomUser.Roles.CUSTOMER:
        return render(request, 'profile_customer.html')
    if user.role == CustomUser.Roles.SELLER:
        return render(request, 'profile_seller.html')
    if user.role == CustomUser.Roles.STAFF:
        return redirect(reverse('admin:index'))

@login_required
def profile_edit(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'پروفایل شما با موفقیت بروزرسانی شد')
            return redirect('account:profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile_edit.html', {'form': form})