from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate

from .forms import CustomUserCreateForm , CustomUserLoginForm

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreateForm(request.POST)
        if form.is_valid():
            form.cleaned_data.pop('confirm_password', None)
            password = form.cleaned_data.pop('password', None)
            user = form.save(commit=False)
            if password:
                user.set_password(password)
                user.save()
                messages.success(request, 'تبریک! ثبت نام شما با موفقیت انجام شد.')
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('page:home')
    else:
        form = CustomUserCreateForm()

    return render(request, 'user/register.html', {'form': form})


def logout_view(request):
    if not request.user.is_authenticated:
        return redirect('user:login')
    logout(request)
    messages.info(request, 'شما با موفقیت خارج شدید.')
    return redirect('page:home')

def login_view(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data.get('phone')
            password = form.cleaned_data.get('password')
            user = authenticate(request, phone=phone, password=password)
            if user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, 'خوش آمدید! ورود با موفقیت انجام شد.')
                return redirect('page:home')
            else:
                form.add_error('phone', 'شماره موبایل یا رمز عبور اشتباه است.')
    else:
        form = CustomUserLoginForm()
    return render(request, 'user/login.html', {'form': form})