from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST

validator = EmailValidator()


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def bank(request):
    return render(request, 'bank.html')

@require_POST
def subscribe(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            validator(email)
            messages.success(request, "ایمیل شما با موفقیت ثبت شد.")
            return redirect("page:home")
        
        except ValidationError:
            messages.error(request, "ایمیل وارد شده اشتباه است!")
            return redirect("page:home")
            
    return redirect("page:home")
