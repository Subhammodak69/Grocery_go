from django.shortcuts import redirect
from functools import wraps

def enduser_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 2:  # ENDUSER role
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 1:  # ADMIN role
            return redirect('admin_login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def delivery_worker_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 3:  # Delivery Worker role
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def homeNavigate(view_func):
    def _wrapped_view(request,*args, **kwargs):
        if request.user.is_authenticated:
            if request.user.role == 3:
                return redirect('delivery_worker_home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def anonymous_required(redirect_url='dashboard'):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_url)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator