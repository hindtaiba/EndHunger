from email.message import EmailMessage
from django.views.decorators.csrf import csrf_protect
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
from django.contrib.sessions.models import Session
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.shortcuts import render
from django.http import HttpResponse
from .forms import SMSForm
import requests 
from django.http import HttpRequest


def home(request):
    restaurants = Restaurant.objects.all() # Fetch only the first four restaurants
    return render(request, 'index.html',{'restaurants':restaurants})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Perform any necessary validations on the form data

        # Send email notification
        send_mail(
            subject='Contact Us: ' + subject,
            message='Name: ' + name + '\nEmail: ' + email + '\n\nMessage: ' + message,
            from_email=email,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
            fail_silently=False
        )
        
    if request.user.is_authenticated:
        if Restaurant.objects.filter(user=request.user).exists():
            user_type = "R"  # User is a restaurant
            status = True
        elif NGO.objects.filter(user=request.user).exists():
            user_type = "N"  # User is an NGO
            status = True
        else:
            user_type = None  # User doesn't have a recognized role
            status = False
    else:
        user_type = None  # User is not authenticated
    return render(request, 'contact.html', {'user': user_type, 'status': status})

def about(request):
    if request.user.is_authenticated:
        if Restaurant.objects.filter(user=request.user).exists():
            user_type = "R"  # User is a restaurant
            status = True
        elif NGO.objects.filter(user=request.user).exists():
            user_type = "N"  # User is an NGO
            status = True
        else:
            user_type = None  # User doesn't have a recognized role
            status = False
    else:
        user_type = None  # User is not authenticated
    return render(request, 'about.html', {'user': user_type, 'status': status})

def loginRegister(request):
    return render(request, 'login-register.html')


def charity_view(request):
    user_type = None
    status = False
    if request.user.is_authenticated:
        if Restaurant.objects.filter(user=request.user).exists():
            user_type = "R"  # User is a restaurant
            status = True
            available_charities = NGO.objects.filter(is_verified=True)  # Fetch verified NGOs
        elif NGO.objects.filter(user=request.user).exists():
            user_type = "N"  # User is an NGO
            status = True
        else:
            user_type = None  # User doesn't have a recognized role

    return render(request, 'charity.html', {'user': user_type, 'status': status, 'charities': available_charities})

def restaurant_view(request):
    user_type = None
    status = False

    if request.user.is_authenticated:
        if NGO.objects.filter(user=request.user).exists():
            user_type = "N"  # User is an NGO
            status = True
            available_restaurants = Restaurant.objects.filter(is_verified=True)  # Fetch verified restaurants
        else:
            user_type = None  # User doesn't have a recognized role

    return render(request, 'restaurant.html', {'user': user_type, 'status': status, 'restaurants': available_restaurants})

def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    return render(request, 'restaurant_detail.html', {'restaurant': restaurant})


def requestsR_view(request):
    if request.user.is_authenticated:
        if Restaurant.objects.filter(user=request.user).exists():
            user_type = "R"  # User is a restaurant
            status = True
        elif NGO.objects.filter(user=request.user).exists():
            user_type = "N"  # User is an NGO
            status = True
        else:
            user_type = None  # User doesn't have a recognized role
            status = False
    else:
        user_type = None  # User is not authenticated
    return render(request,'requestsR.html', {'user': user_type, 'status': status})

def requestsN_view(request):
    return render(request,'requestsN.html')


def register(request):
    if request.method == 'POST':
        password = request.POST['password']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        location=request.POST['location']
        choice = request.POST.get('choice')

        try:
            user = User.objects.get(username=name)
            return render(request, 'login-register.html')
        except User.DoesNotExist:
            # add this if only active users log in ,is_active=False
            user = User.objects.create_user(username=name, password=password, is_active = False)

            print()
            if choice == 'Restaurant':
                restaurant = Restaurant(name=name, contact_email=email, contact_phone=phone, user=user,location=location, is_verified= False)
                restaurant.save()
                print('Registered as a Restaurant')
            elif choice == 'Charity':
                ngo = NGO(name=name, contact_email=email, contact_phone=phone, user=user,location=location,is_verified= False)
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
            from_email=settings.DEFAULT_FROM_EMAIL,
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
            return redirect('/login/', {'message': 'Your accoumt is verified now'})
        except Restaurant.DoesNotExist:
            try:
                ngo = NGO.objects.get(user=user)
                user.is_active= True
                ngo.is_verified = True
                ngo.save()
                return redirect('/login/', {'message': 'Your accoumt is verified now'})
            except NGO.DoesNotExist:
                messages.error(request, 'Associated restaurant or Charity does not exist.')
                return render(request, 'login-register.html', {'message': 'Associated restaurant or Charity does not exist. Verification failed'})
    else:
        messages.error(request, 'Invalid verification link.')
        return render(request, 'login-register.html', {'message': 'Invalid verification link. Verification failed'})
    


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
    
# def dashboard(request, user):
#     if user == "AnonymousUser":
#         return redirect('home')

#     show_get_started_modal = False
#     if request.user.is_authenticated and not (request.user.is_superuser or request.user.profile.is_modal_displayed):
#         show_get_started_modal = True
#         request.user.profile.is_modal_displayed = True
#         request.user.profile.save()

#     return render(request, 'index.html', {'user': user, 'show_get_started_modal': show_get_started_modal})


def dashboard(request, user):
    print(user)
    status = False
    if request.user:
        if user == "R":
            restaurant = Restaurant.objects.get(user=request.user)
            print(restaurant)
            name = restaurant
        elif user == "N":
            ngo = NGO.objects.get(user=request.user)
            name = ngo
        status = request.user
    if user == "AnonymousUser":
        name=""
        return redirect('home')
    user_name=""

    return render(request, 'index.html', {'user': user, "status": status, 'user_name':name})


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
        recipient_list = [email]
        try:
            ngo = NGO.objects.get(contact_email=email)
            user = ngo.user
        except NGO.DoesNotExist:
            # User not found in the NGO model, search in the Restaurant model
            try:
                restaurant = Restaurant.objects.get(contact_email=email)
                user = restaurant.user
            except Restaurant.DoesNotExist:
                # User not found in both the NGO and Restaurant models
                # Handle the case when the user does not exist
                # You can show an error message or redirect the user to an appropriate page
                return HttpResponse("User does not exist.")
        
        current_site = get_current_site(self.request)
        
        message = render_to_string('password_reset_email.html', {
            'user': user,
            'protocol': 'http',
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        email_message = EmailMessage(
        subject= subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=recipient_list,
        )
        email_message.content_subtype = 'html'
        email_message.send()
        
        return super().form_valid(form)




class PasswordResetConfirmationView(PasswordResetConfirmView):
    form_class = PasswordResetConfirmationForm
    template_name = 'password_reset_confirm.html'
    success_url = '/password_reset/complete/'
    print("done")
    


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'


import json
from datetime import date
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from keras.models import load_model


@login_required
def add_donation(request):
    # Fetch the current restaurant
    restaurant = get_object_or_404(Restaurant, user=request.user)

    # Fetch the updated list of donations for the current restaurant
    donations = Donation.objects.filter(restaurant=restaurant)

    # Group donations based on their status
    todo_donations = donations.filter(requested=False)
    inprogress_donations = donations.filter(requested=True, confirmed=False)
    done_donations = donations.filter(requested=True, confirmed=True)

    if Restaurant.objects.filter(user=request.user).exists():
        user_type = "R"  # User is a restaurant
        status = True
    elif NGO.objects.filter(user=request.user).exists():
        user_type = "N"  # User is an NGO
        status = True
    else:
        user_type = None  # User doesn't have a recognized role
        status = False

    ngos = NGO.objects.all()

    if restaurant.name == "Aquaria":
        ngos = ngos.filter(location__in=['Mina', 'Al-Tal'])
    
    if restaurant.name == "hallab":
        ngos = ngos.filter(location__in=['Tripoli Zeitoun', 'Al-Mina'])

    if restaurant.name == "Baytuna":
        ngos = ngos.filter(location__in=['Tripoli Zeitoun', 'Al-Mina','Al-Tabbaneh'])



    


    if request.method == 'POST':
        if 'next_button' in request.POST:
            # Handle the next button (form part 1)
            # Process the form data from the first part of the form
            quantity_value = int(request.POST.get('food_quantity'))
            expiration_date = request.POST.get('expiration_date')
            food_condition = request.POST.get('food_condition')
            packaging = request.POST.get('packaging')
            transportation = request.POST.get('transportation')

            if quantity_value < 50:
                quantity_category = "less than 50"
            elif 50 <= quantity_value < 100:
                quantity_category = "50-100"
            elif 100 <= quantity_value < 200:
                quantity_category = "100-200"
            elif 200 <= quantity_value < 500:
                quantity_category = "200-500"
            else:
                quantity_category = "more than 500"

            # Create a new Donation object without the missing fields
            donation = Donation.objects.create(
                restaurant=restaurant,
                quantity=quantity_category,
                expiration_date=expiration_date,
                food_condition=food_condition,
                packaging=packaging,
                transportation=transportation
            )

            # Store the donation ID in the session or database, depending on your requirements
            request.session['donation_id'] = donation.id

            # Redirect to the second part of the form
            return render(request, 'second_form.html', {'ngos': ngos, 'user':user_type, 'status':status})  # Replace with the URL for the second form

    context = {
        'donations': donations,
        'ngos': ngos,
        'todo_donations': todo_donations,
        'inprogress_donations': inprogress_donations,
        'done_donations': done_donations,
        'user': user_type,
        'status': status
    }

    return render(request, 'donations.html', context)


def submit_donation(request):
    # Fetch the current restaurant
    restaurant = get_object_or_404(Restaurant, user=request.user)

    # Fetch the updated list of donations for the current restaurant
    donations = Donation.objects.filter(restaurant=restaurant)

    # Group donations based on their status
    todo_donations = donations.filter(requested=False)
    inprogress_donations = donations.filter(requested=True, confirmed=False)
    done_donations = donations.filter(requested=True, confirmed=True)

    if Restaurant.objects.filter(user=request.user).exists():
        user_type = "R"  # User is a restaurant
        status = True
    elif NGO.objects.filter(user=request.user).exists():
        user_type = "N"  # User is an NGO
        status = True
    else:
        user_type = None  # User doesn't have a recognized role
        status = False

    filtered_ngos = NGO.objects.all()

    if restaurant.name == "Aquaria":
        filtered_ngos = filtered_ngos.filter(location='Al-Mina')

    if request.method == 'POST':
        # Retrieve the form data from the second part of the form
        ngo = request.POST.get('ngo')
        delivery_time = request.POST.get('delivery_time')

        donation_id = request.session.get('donation_id')
        if donation_id:
            donation = get_object_or_404(Donation, id=donation_id)
            ngo = get_object_or_404(NGO, name=ngo)

            # Update the existing Donation object with the missing fields
            donation.ngo = ngo
            donation.delivery_time = delivery_time
            donation.save()

            # Perform any necessary actions with the complete form data

            # Clear the donation ID from the session or database
            del request.session['donation_id']

            context = {
                'donations': donations,
                'todo_donations': todo_donations,
                'inprogress_donations': inprogress_donations,
                'done_donations': done_donations,
                'ngos': filtered_ngos,
                'user': user_type,
                'status': status
            }

            # Redirect to a success page or perform any other desired actions
            return render(request, 'donations.html', context)  # Replace with the URL for the success page

    context = {
        'donations': donations,
        'todo_donations': todo_donations,
        'inprogress_donations': inprogress_donations,
        'done_donations': done_donations,
        'ngos': filtered_ngos,
        'user': user_type,
        'status': status
    }

    return render(request, 'donations.html', context)




@login_required
def view_donations(request):
    if request.user.is_authenticated:
        if Restaurant.objects.filter(user=request.user).exists():
            user_type = "R"  # User is a restaurant
            status = True
        elif NGO.objects.filter(user=request.user).exists():
            user_type = "N"  # User is an NGO
            status = True
        else:
            user_type = None  # User doesn't have a recognized role
            status = False
    else:
        user_type = None  # User is not authenticated
    # Check if the user is associated with a restaurant
    try:
        ngo = NGO.objects.get(user=request.user)
    except NGO.DoesNotExist:
        return render(request, 'browse_donations.html', {'message': 'User does not have a related restaurant.'})
    
    # Fetch the donations for the current restaurant
    donations = Donation.objects.filter(ngo=ngo)
    
    return render(request, 'browse_donations.html', {'donations': donations, 'ngo': ngo, 'user': user_type, 'status': status} )

def request_donation(request, donation_name):
    donation = get_object_or_404(Donation, pk=donation_name)

    if donation.confirmed:
        # Donation is already confirmed, do nothing
        pass
    elif donation.requested:
        # Undo the donation request
        donation.requested = False
        donation.save()

        # Send email to the restaurant notifying them of the request undo
        restaurant_email = donation.restaurant.contact_email
        restaurant_name = donation.restaurant.name
        ngo_name=donation.ngo.name
        send_request_undo_email(restaurant_email, restaurant_name,ngo_name)
    else:
        # Mark the donation as requested by the NGO
        donation.requested = True
        donation.save()

        # Send email to the restaurant notifying them of the new request
        restaurant_email = donation.restaurant.contact_email
        restaurant_name = donation.restaurant.name
        ngo_name=donation.ngo.name
        send_request_email(restaurant_email, restaurant_name,ngo_name)

    return redirect('/browse_donations/')


def send_request_email(restaurant_email, restaurant_name, ngo_name):
    subject = 'New Donation Request'
    message = f'Dear {restaurant_name}, please check your FoodBridge account. You might have new requests available from {ngo_name}.'

    email = EmailMessage(subject, message, from_email=settings.DEFAULT_FROM_EMAIL, to=[restaurant_email])
    email.send()

def send_request_undo_email(restaurant_email, restaurant_name, ngo_name):
    subject = 'Donation Request Undone'
    message = f'Dear {restaurant_name}, the donation request from {ngo_name} has been undone. Please check your FoodBridge account.'

    email = EmailMessage(subject, message, from_email=settings.DEFAULT_FROM_EMAIL, to=[restaurant_email])
    email.send()

def confirm_donation(request, donation_id):
    donation = get_object_or_404(Donation, pk=donation_id)

    if not donation.confirmed and donation.requested:
        # Confirm the donation
        donation.confirmed = True
        donation.save()
        
        #Send confirmation email to NGO
        ngo_email= donation.ngo.contact_email
        restaurant_location= donation.restaurant.location 
        restaurant_number=donation.restaurant.contact_phone
        ngo_name=donation.ngo.name
        restaurant_name=donation.restaurant.name
       
        send_confirmation_email(ngo_email,restaurant_location,restaurant_number,ngo_name,restaurant_name)

    return redirect('/donate/')

def send_confirmation_email(ngo_email, restaurant_location,restaurant_number,ngo_name,restaurant_name):
    subject = 'Donation Confirmation'
    template = 'donation_confirmation.html'  # Path to your email template

    context = {
        'restaurant_location': restaurant_location,
        'restaurant_number': restaurant_number,
        'ngo_name': ngo_name,
        'restaurant_name':restaurant_name
    }
    email_body = render_to_string(template, context)

    email = EmailMessage(subject, email_body, from_email=settings.DEFAULT_FROM_EMAIL, to=[ngo_email])
    email.content_subtype = 'html'
    email.send()


@login_required
def update_profile(request):
    if request.method == 'POST':
        profile_picture = request.FILES.get('profile_picture')

        if hasattr(request.user, 'restaurant'):
            restaurant = request.user.restaurant
            restaurant.profile_picture = profile_picture
            restaurant.name = request.POST.get('name', restaurant.name)
            restaurant.contact_phone = request.POST.get('contact_phone', restaurant.contact_phone)
            restaurant.location = request.POST.get('location', restaurant.location)
            restaurant.cuisine_type = request.POST.get('cuisine_type', restaurant.cuisine_type)
            restaurant.description = request.POST.get('description', restaurant.description)
            restaurant.save()
             # Update the username in the User model
            user = restaurant.user
            user.username = restaurant.name  # Update the username with the new name
            user.save()
            
        elif hasattr(request.user, 'ngo'):
            ngo = request.user.ngo
            ngo.profile_picture = profile_picture
            ngo.name = request.POST.get('name', ngo.name)
            ngo.contact_phone = request.POST.get('contact_phone', ngo.contact_phone)
            ngo.location = request.POST.get('location', ngo.location)
            ngo.capacity = request.POST.get('capacity')
            ngo.description = request.POST.get('description')
            ngo.save()
          # Update the username in the User model
            user = ngo.user
            user.username = ngo.name  # Update the username with the new name
            user.save()
        return redirect('home')

    if hasattr(request.user, 'restaurant'):
        restaurant = request.user.restaurant
        initial_data = {
            'name': restaurant.name,
            'contact_phone': restaurant.contact_phone,
            'location': restaurant.location,
            'cuisine_type': restaurant.cuisine_type,
            'description': restaurant.description,
            'profile_picture_url': restaurant.profile_picture.url if restaurant.profile_picture else '',
        }
        return render(request, 'profile.restaurant.html', initial_data)
    elif hasattr(request.user, 'ngo'):
        ngo = request.user.ngo
        initial_data = {
            'name': ngo.name,
            'contact_phone': ngo.contact_phone,
            'location': ngo.location,
            'capacity': ngo.capacity,
            'description': ngo.description,
            'profile_picture_url': ngo.profile_picture.url if ngo.profile_picture else '',
        }
        return render(request, 'profile.ngo.html', initial_data)
    else:
        return redirect('home')