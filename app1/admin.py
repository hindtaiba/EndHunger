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

from django.contrib import admin
from django.shortcuts import redirect
import requests

from django.contrib import admin
from django.shortcuts import redirect, reverse
import requests

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'contact_email', 'contact_phone', 'cuisine_type', 'description')
    actions = ['send_sms_to_restaurants']
    readonly_fields = ()

    def send_sms_to_restaurants(self, request, queryset):
        username = "naderbakir@gmail.com"
        password = "qfzjui"
        advert_message = "REMINDER to make a difference today and change lives with FoodBridge!"

        for restaurant in queryset:
            number = restaurant.contact_phone

            url = f"http://unosms.us/api.php?user={username}&pass={password}&to={number}&from=fsegorg&msg={advert_message}"

            response = requests.get(url)

            if response.status_code == 200:
                self.message_user(request, f"SMS sent to {number} successfully!")
            else:
                self.message_user(request, f"Failed to send SMS to {number}. Error: {response.text}")

        change_list_url = reverse('admin:app1_restaurant_changelist')  # Replace 'app1' with your app name
        return redirect(change_list_url)  # Redirect to the restaurant change list page

    send_sms_to_restaurants.short_description = "Send Reminder SMS"






class NGOAdmin(admin.ModelAdmin):
    list_display = ('name','location','contact_email','contact_phone','capacity','description')
    actions = ['send_sms_to_restaurants']
    readonly_fields = ()

    def send_sms_to_restaurants(self, request, queryset):
        username = "naderbakir@gmail.com"
        password = "qfzjui"
        advert_message = "REMINDER to make a difference today and change lives with FoodBridge!"

        for restaurant in queryset:
            number = restaurant.contact_phone

            url = f"http://unosms.us/api.php?user={username}&pass={password}&to={number}&from=fsegorg&msg={advert_message}"

            response = requests.get(url)

            if response.status_code == 200:
                self.message_user(request, f"SMS sent to {number} successfully!")
            else:
                self.message_user(request, f"Failed to send SMS to {number}. Error: {response.text}")

        change_list_url = reverse('admin:app1_restaurant_changelist')  # Replace 'app1' with your app name
        return redirect(change_list_url)  # Redirect to the restaurant change list page

    send_sms_to_restaurants.short_description = "Send Reminder SMS"


class DonationAdmin(admin.ModelAdmin):
    confirmed = models.BooleanField(default=False)
    list_display = ('name','restaurant', 'ngo', 'delivery_time','created_on','confirmed','expiration_date','requested','quantity')
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
    


admin.site.register(Donation, DonationAdmin)
admin.site.register(NGO, NGOAdmin)
admin.site.register(Restaurant,RestaurantAdmin)