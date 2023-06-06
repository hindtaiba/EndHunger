from email.message import EmailMessage
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Restaurant, NGO
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



# Create your views here.
def home(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def loginRegister(request):
    return render(request, 'login-register.html')

def requests_view(request):
    return render(request,'#')

def donate_view(request):
    return render(request,'#')

def charity_view(request):
    return render(request,'#')

def browse_food_view(request):
    return render(request,'#')

def restaurant_view(request):
    return render(request,'#')

def confirmations_view(request):
    return render(request,'#')


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
    auth.logout(request)
    print('logout')
    return render(request,'index.html')