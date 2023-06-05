from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

class DonationAdmin(admin.ModelAdmin):
    list_display = ('restaurant','ngo','donation_date','delivery_time','posted','confirmed')
    readonly_fields = ( )

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
        if  hasattr(request.user, 'ngo'):  # Editing an existing user
            return self.readonly_fields + ('confirmed',)
        if  hasattr(request.user, 'restaurant'):  # Editing an existing user
            return self.readonly_fields + ('donation_date','delivery_time')

        return self.readonly_fields
    
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'expiration_date', 'quantity', 'packaging_type', 'food_type','restaurant')
    readonly_fields = ()

    def get_queryset(self, request):
        # Only display food items for the current restaurant user
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            # Superusers can add and view and everything
            return qs
        if hasattr(request.user, 'restaurant'):
            return qs.filter(restaurant=request.user.restaurant)
        else:
            # Non-restaurant users won't see any food items
            return qs.none()

    def get_readonly_fields(self, request, obj=None):
        if hasattr(request.user, 'restaurant'):  # Editing an existing user
            return self.readonly_fields + ('name', 'description', 'expiration_date', 'quantity', 'packaging_type', 'food_type', 'restaurant')

        return self.readonly_fields


admin.site.register(FoodItem, FoodItemAdmin)
admin.site.register(Donation,DonationAdmin)
admin.site.register(Restaurant)
admin.site.register(NGO)
# admin.site.register(FoodItem)
