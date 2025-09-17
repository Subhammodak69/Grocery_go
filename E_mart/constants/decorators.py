from django.shortcuts import redirect

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
