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
        elif request.user.is_authenticated and request.path == '/login/':
            if request.user.groups.filter(name='PermissionOfRestaurant').exists():
                return redirect('/dashboard/R/')
            elif request.user.groups.filter(name='ngo').exists():
                return redirect('/dashboard/N/')
        elif request.user.is_authenticated and request.path == '/register/':
            if request.user.groups.filter(name='PermissionOfRestaurant').exists():
                return redirect('/dashboard/R/')
            elif request.user.groups.filter(name='ngo').exists():
                return redirect('/dashboard/N/')

        return self.get_response(request)
    
from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore


# class DonationMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         # Check if the user is on the donations page
#         if request.path == '/donations/':
#             # Retrieve the donation data from the session
#             donation_data = request.session.get('donation_data')
#             if donation_data:
#                 # Pass the donation data to the template context
#                 request.donation_data = donation_data
#                 # Clear the donation data from the session
#                 del request.session['donation_data']

#         response = self.get_response(request)

#         # Check if the user is submitting the donation form
#         if request.method == 'POST' and request.path == '/donations/':
#             # Save the donation data to the session
#             request.session['donation_data'] = {
#                 'ngo': request.POST.get('ngo'),
#                 'donation_date': request.POST.get('donation_date'),
#                 'delivery_time': request.POST.get('delivery_time'),
#                 'expiration_date': request.POST.get('expiration_date'),
#             }

#         return response

