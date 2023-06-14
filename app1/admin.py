from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.shortcuts import render
from .forms import SMSForm
import requests 
from django.core.mail import send_mail


class NGOAdmin(admin.ModelAdmin):
    list_display = ('name','user','location','contact_email','contact_phone','review','category')
    readonly_fields = ( )

class DonationAdmin(admin.ModelAdmin):
    confirmed = models.BooleanField(default=False)
    list_display = ('name','restaurant', 'ngo', 'donation_date', 'delivery_time','created_on','confirmed','expiration_date','requested')
    readonly_fields = ()

    def get_queryset(self, request):
        # Only display donations for the current user
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            # Superusers can see all donations
            return qs
        elif hasattr(request.user, 'ngo'):
            return qs.filter(ngo=request.user.ngo)
        elif hasattr(request.user, 'restaurant'):
            return qs.filter(restaurant=request.user.restaurant)
        else:
            # Non-ngo or Non-restaurant users won't see any donations
            return qs.none()

    def get_readonly_fields(self, request, obj=None):
        if hasattr(request.user, 'ngo'):  # Editing an existing NGO user
            return self.readonly_fields + ('confirmed',)
        if hasattr(request.user, 'restaurant'):  # Editing an existing restaurant user
            return self.readonly_fields + ('donation_date', 'delivery_time')

        return self.readonly_fields
    
class DonationRequestAdmin(admin.ModelAdmin):
    list_display = ('donation', 'ngo','confirmed')
    readonly_fields = ()

    def get_queryset(self, request):
        # Only display donation requests for the current user
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            # Superusers can see all donation requests
            return qs
        elif hasattr(request.user, 'ngo'):
            return qs.filter(ngo=request.user.ngo)
        elif hasattr(request.user, 'restaurant'):
            return qs.filter(donation__restaurant=request.user.restaurant)
        else:
            # Non-ngo or Non-restaurant users won't see any donation requests
            return qs.none()

    def get_readonly_fields(self, request, obj=None):
        if hasattr(request.user, 'ngo'):  # Editing an existing NGO user
            return self.readonly_fields + ('confirmed',)

        return self.readonly_fields

admin.site.register(Donation, DonationAdmin)
admin.site.register(DonationRequest, DonationRequestAdmin)
admin.site.register(NGO, NGOAdmin)

    
# class DonationAdmin(admin.ModelAdmin):
#     list_display = ('restaurant','ngo','donation_date','delivery_time','posted','confirmed')
#     readonly_fields = ( )

#     def get_queryset(self, request):
#         # Only display donations for the current user
#         qs = super().get_queryset(request)
#         if request.user.is_superuser:
#             # Superusers can see all donations
#             return qs
#         elif hasattr(request.user, 'ngo'):
#             return qs.filter(ngo=request.user.ngo)
#         elif hasattr(request.user, 'restaurant'):
#             return qs.filter(restaurant=request.user.restaurant)
#         else:
#             # Non-ngo or Non-restaurant users won't see any donations
#             return qs.none()

#     def get_readonly_fields(self, request, obj=None):
#         if  hasattr(request.user, 'ngo'):  # Editing an existing user
#             return self.readonly_fields + ('confirmed',)
#         if  hasattr(request.user, 'restaurant'):  # Editing an existing user
#             return self.readonly_fields + ('donation_date','delivery_time')

#         return self.readonly_fields
    
# class FoodItemAdmin(admin.ModelAdmin):
#     list_display = ('name', 'description', 'expiration_date', 'quantity', 'packaging_type', 'food_type','restaurant')
#     readonly_fields = ()
    
#     def mark_events_completed(modeladmin, request, queryset):
#         pass
    
#     actions = [mark_events_completed]


    
#     def get_queryset(self, request):
#         # Only display food items for the current restaurant user
#         qs = super().get_queryset(request)
#         if request.user.is_superuser:
#             # Superusers can add and view and everything
#             return qs
#         if hasattr(request.user, 'restaurant'):
#             return qs.filter(restaurant=request.user.restaurant)
#         else:
#             # Non-restaurant users won't see any food items
#             return qs.none()

#     def get_readonly_fields(self, request, obj=None):
#         if hasattr(request.user, 'restaurant'):  # Editing an existing user
#             return self.readonly_fields + ('name', 'description', 'expiration_date', 'quantity', 'packaging_type', 'food_type', 'restaurant')

#         return self.readonly_fields





from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'location', 'contact_email', 'contact_phone')
    actions = ['send_sms_to_restaurants', 'send_email_to_restaurants']
    readonly_fields = ()

    def send_sms_to_restaurants(self, request, queryset):
        if request.method == 'POST':
            form = SMSForm(request.POST)
            # if form.is_valid():
            #     print('Riwa')
            # else:
            #     print(form.errors)
            # print('Hind', form.is_valid())
            # # print(form.message1)
            # msg = form.cleaned_data['messages']
            # print('Riwa ' , msg)
            if form.is_valid():
                msg = form.cleaned_data['message']
                print('Riwa ' , msg)
                username = "naderbakir@gmail.com"
                password = "qfzjui"

                for restaurant in queryset:
                    number = restaurant.contact_phone
                    name = restaurant.name

                    url = f"http://unosms.us/api.php?user={username}&pass={password}&to={number}&from=fsegorg&msg={message}"

                    response = requests.get(url)

                    if response.status_code == 200:
                        messages.success(request, f"SMS sent to {number} successfully!")
                    else:
                        messages.error(request, f"Failed to send SMS to {number}. Error: {response.text}")
                
                return redirect('admin:app_restaurant_changelist')
            else:
                print(form.errors)
        else:
            form = SMSForm()

        context = {
            'form': form,
            'queryset': queryset,
        }
        
        return render(request, 'send_sms.html', context)

    send_sms_to_restaurants.short_description = "Send SMS to selected restaurants"


    def send_email_to_restaurants(modeladmin, request, queryset):
        for restaurant in queryset:
            email = restaurant.contact_email
            name = restaurant.name

            subject = f"Hello, {name}!"
            message = f"Dear {name},\n\nThis is a personalized message for your restaurant."
            from_email = "endhunger4@gmail.com"  # Replace with your email address or a valid sender email
            recipient_list = [email]

            send_mail(subject, message, from_email, recipient_list)

        # Provide a feedback message for the admin action
        message = f"Email sent to selected restaurants: {', '.join([restaurant.name for restaurant in queryset])}"
        modeladmin.message_user(request, message)

    send_email_to_restaurants.short_description = "Send Email to selected restaurants"

admin.site.register(Restaurant,RestaurantAdmin)
