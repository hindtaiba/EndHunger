from django.shortcuts import redirect
from django.urls import reverse

class RedirectHomeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (request.user.is_authenticated and request.path == '/'):
            if request.user.groups.filter(name='PermissionOfRestaurant').exists():
                return redirect('/dashboard/R/')
            elif request.user.groups.filter(name='ngo').exists():
                return redirect('/dashboard/N/')
        elif request.user.is_authenticated and request.path == '/login-register/':
            if request.user.groups.filter(name='PermissionOfRestaurant').exists():
                return redirect('/dashboard/R/')
            elif request.user.groups.filter(name='ngo').exists():
                return redirect('/dashboard/N/')

        return self.get_response(request)
