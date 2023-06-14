from django.shortcuts import redirect, HttpResponse, render
from django.urls import reverse
from django.contrib.auth import logout

class RedirectHomeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and request.path.startswith('/dashboard/'):
            return redirect('/login/')
        elif request.user.is_authenticated and request.path in ('/login-register/', '/login/', '/register/'):
            if request.user.groups.filter(name='PermissionOfRestaurant').exists():
                return redirect('/dashboard/R/')
            elif request.user.groups.filter(name='PermissionOfNGO').exists():
                return redirect('/dashboard/N/')
            else:
                return redirect ('/logout/')
        elif request.user.is_authenticated and request.path == '/':
            if request.user.groups.filter(name='PermissionOfRestaurant').exists():
                return redirect('/dashboard/R/')
            elif request.user.groups.filter(name='PermissionOfNGO').exists():
                return redirect('/dashboard/N/')
        elif not request.user.is_authenticated and request.path == '/logout/':
            return redirect('/')
        if request.user.is_authenticated and request.user.groups.filter(name='PermissionOfRestaurant').exists():
            if  request.path == '/dashboard/N/':
                return redirect('/dashboard/R/')
        elif request.user.is_authenticated and request.user.groups.filter(name='PermissionOfNGO').exists():
            if  request.path == '/dashboard/R/':
                return redirect('/dashboard/N/')
        elif request.user.is_authenticated and request.path.startswith('/admin/') and (request.user.groups.filter(name='PermissionOfNGO').exists() or request.user.groups.filter(name='PermissionOfRestaurant').exists()):
            return redirect(reverse('admin:index'))

        return self.get_response(request)
    
# class PermissionMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         # Check permission logic here
#         if not request.user.has_perm('app1.can_donate_food'):
#             return HttpResponse('You do not have permission to donate food.')

#         response = self.get_response(request)
#         return response
    
import logging

class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger(__name__)

    def __call__(self, request):
        # Logging logic before processing the request
        self.logger.info('Request: {} {}'.format(request.method, request.path))
        
        response = self.get_response(request)
        
        # Logging logic after processing the request
        if isinstance(response, HttpResponse):
            self.logger.info('Response: {} {}'.format(response.status_code, response.reason_phrase))
        else:
            self.logger.warning('Response: {}'.format(response))

        return response
