from email.message import EmailMessage
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from app1.forms import PasswordResetConfirmationForm, PasswordResetRequestForm
from app1 import forms
from .models import Restaurant, NGO, Donation
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.html import strip_tags
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.sessions.models import Session
    
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)



# Create your views here.
def home(request):
    return render(request, 'index.html')

def contact(request):
    if request.user.is_authenticated:
        if Restaurant.objects.filter(user=request.user).exists():
            user_type = "R"  # User is a restaurant
        elif NGO.objects.filter(user=request.user).exists():
            user_type = "N"  # User is an NGO
        else:
            user_type = None  # User doesn't have a recognized role
    else:
        user_type = None  # User is not authenticated
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def loginRegister(request):
    return render(request, 'login-register.html')

def requests_view(request):
    return render(request,'requestsR.html')

def donate_view(request):
    return render(request,'donations.html')

def charity_view(request):
    return render(request,'#')

def browse_donations(request):
    return render(request,'browse_donations.html')

def restaurant_view(request):
    return render(request,'#')


def requestsR_view(request):
    return render(request,'requestsR.html')


def register(request):
    if request.method == 'POST':
        password = request.POST['password']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        choice = request.POST.get('choice')

        try:
            user = User.objects.get(username=name)
            return render(request, 'login-register.html')
        except User.DoesNotExist:
            # add this if only active users log in ,is_active=False
            user = User.objects.create_user(username=name, password=password, is_active = False)

            print()
            if choice == 'Restaurant':
                restaurant = Restaurant(name=name, contact_email=email, contact_phone=phone, user=user, is_verified= False)
                restaurant.save()
                print('Registered as a Restaurant')
            elif choice == 'Charity':
                ngo = NGO(name=name, contact_email=email, contact_phone=phone, user=user, is_verified= False)
                ngo.save()
                print('Registered as an NGO')
            else:
                # Handle registration for other roles if needed
                pass
            
            # Send email for account activation
            current_site = get_current_site(request)
            mail_subject = 'Activate Your Account'
            message = render_to_string('verify_email.html', {
                'user': user,
                'protocol': 'http',
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            email_message = EmailMessage(
            subject=mail_subject,
            body=message,
            from_email='endhunger4@gmail.com',
            to=[email],
            )
            email_message.content_subtype = 'html'
            email_message.send()
            print('Registered Successfully')
            return render(request, 'login-register.html')
        
        except IntegrityError as e:
            error_message = f"An error occurred during registration: {str(e)}"
            return render(request, 'login-register.html', {'error_message': error_message})

        except ValidationError as e:
            error_message = e.message
            return render(request, 'login-register.html', {'error_message': error_message})
    else:
        return render(request, 'login-register.html')


def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        try:
            restaurant = Restaurant.objects.get(user=user)
            user.is_active = True
            restaurant.is_verified = True
            restaurant.save()
            return render(request, 'login-register.html', {'message': 'Your account is verified'})
        except Restaurant.DoesNotExist:
            try:
                ngo = NGO.objects.get(user=user)
                user.is_active= True
                ngo.is_verified = True
                ngo.save()
                return render(request, 'login-register.html', {'message': 'Your account is verified'})
            except NGO.DoesNotExist:
                messages.error(request, 'Associated restaurant or Charity does not exist.')
                return redirect('verification_failed')
    else:
        messages.error(request, 'Invalid verification link.')
        return redirect('verification_failed')
    


def login(request):
    if request.method == 'POST':
        try:
            # Check User in DB
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)  # Renamed 'user_authenticate' to 'user'
            if user is not None:  # Simplified the condition
                if user.is_active:
                    try:
                        restaurant = Restaurant.objects.get(user=user)  # Moved 'restaurant' and 'ngo' inside this block
                        if restaurant.is_verified:
                            auth.login(request, user)
                            print('Restaurant has been Logged')
                            return redirect('dashboard', user="R")
                        else:
                            return render(request, 'login-register.html', {'message': 'Your email is not verified yet'})
                    except Restaurant.DoesNotExist:
                        try:
                            ngo = NGO.objects.get(user=user)
                            if ngo.is_verified:
                                auth.login(request, user)
                                print('NGO has been Logged')
                                return redirect('dashboard', user="N")
                            else:
                                return render(request, 'login-register.html', {'message': 'Your email is not verified yet'})
                        except NGO.DoesNotExist:
                            return redirect('/')
                else:
                    messages.error(request, 'Your account is disabled.')
            else:
                print('Login Failed')
                return render(request, 'login-register.html', {'message': 'Invalid email or password'})
        except:
            print('Login Failed')
            return render(request, 'login-register.html')
    else:
        return render(request, 'login-register.html', {"user": None})

def dashboard(request, user):
    print(user)
    status = False
    if request.user:
        status = request.user
    if user == "AnonymousUser":
        return redirect('home')

    return render(request, 'index.html', {'user': user, "status": status})


def logout_view(request):
    # Clear all sessions associated with the user
    Session.objects.filter(session_key__startswith=request.session.session_key[:10]).delete()
    auth.logout(request)
    print('logout')
    return render(request,'index.html')


class PasswordResetRequestView(PasswordResetView):
    form_class = PasswordResetRequestForm
    template_name = 'password_reset_request.html'
    success_url = '/password_reset/done/'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        subject = 'Password Reset'
        from_email = 'endhunger4@gmail.com'
        recipient_list = [email]

        # Render the password reset email template
        context = {
            'email': email,
            'reset_url': 'password_reset/confirm/<uidb64>/<token>/',  # Replace with your password reset URL
        }
        message = render_to_string('password_reset_email.html', context)

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        return super().form_valid(form)




class PasswordResetConfirmationView(PasswordResetConfirmView):
    form_class = PasswordResetConfirmationForm
    template_name = 'password_reset_confirm.html'
    success_url = '/password_reset/complete/'


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'

@login_required
def add_donation(request):
    # Fetch the updated list of donations for the current restaurant
    restaurant = get_object_or_404(Restaurant, user=request.user)
    donations = Donation.objects.filter(restaurant=restaurant)
    
    if request.method == 'POST':
        ngo = request.POST.get('ngo')
        donation_date = request.POST.get('donation_date')
        delivery_time = request.POST.get('delivery_time')
        expiration_date = request.POST.get('expiration_date')

        # Check if the user is associated with a restaurant
        try:
            restaurant = Restaurant.objects.get(user=request.user)
        except Restaurant.DoesNotExist:
            return render(request, 'error.html', {'message': 'User does not have a related restaurant.'})

        ngo = get_object_or_404(NGO, name=ngo)
        # Create a new Donation object
        donation = Donation.objects.create(
            name=f"{restaurant.name}_{timezone.now().strftime('%Y%m%d')}",
            restaurant=restaurant,
            ngo=ngo,
            donation_date=donation_date,
            delivery_time=delivery_time,
            expiration_date=expiration_date
        )
        
        # Fetch the updated list of donations for the current restaurant
        donations = Donation.objects.filter(restaurant=restaurant)
        # Redirect to the donation success page or any other desired page
        
        return render(request, 'donations.html', {'donations': donations})
    
    return render(request, 'donations.html', {'donations':donations})

@login_required
def requestsN_view(request):
    # Check if the user is associated with a restaurant
    try:
        ngo = NGO.objects.get(user=request.user)
    except NGO.DoesNotExist:
        return render(request, 'requestsN.html', {'message': 'User does not have a related restaurant.'})
    
    # Fetch the donations for the current restaurant
    donations = Donation.objects.filter(ngo=ngo)
    
    return render(request, 'requestsN.html', {'donations': donations, 'ngo': ngo})

from django.shortcuts import render



