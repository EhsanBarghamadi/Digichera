from functools import wraps
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

def store_required(message=None):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not hasattr(request.user, 'store'):
                msg = message or 'شما اجازه دسترسی به این بخش را ندارید'
                messages.error(request, msg)
                return redirect('store:create')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def store_owner_required(model, lookup_field='pk', lookup_url_kwarg=None):
    lookup_url_kwarg = lookup_url_kwarg or lookup_field
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            obj = get_object_or_404(model, **{lookup_field: kwargs.get(lookup_url_kwarg)})
            if not hasattr(request.user, 'store') or obj.store != request.user.store:
                messages.error(request, 'شما اجازه‌ی دسترسی به این مورد را ندارید.')
                return redirect('account:detail')
            request.obj = obj
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator