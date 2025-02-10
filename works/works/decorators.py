from django.http import HttpResponseForbidden
from functools import wraps
from django.shortcuts import redirect

def lider_required(view_func):
    """Protege a página para que apenas Líderes possam acessar"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.session.get('user_type') != 'lider':
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def planejador_required(view_func):
    """Protege a página para que apenas Planejadores possam acessar"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.session.get('user_type') != 'planejador':
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def any_role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.session.get('user_type') not in allowed_roles:
                return redirect('login')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator