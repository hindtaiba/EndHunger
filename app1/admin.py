from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name','user','location','contact_email','contact_phone')
    readonly_fields = ( )
    
class NGOAdmin(admin.ModelAdmin):
    list_display = ('name','user','location','contact_email','contact_phone','review','category')
    readonly_fields = ( )

class DonationAdmin(admin.ModelAdmin):
    confirmed = models.BooleanField(default=False)
    confirmed = models.BooleanField(default=False)
    confirmed = models.BooleanField(default=False)
    list_display = ('name','restaurant', 'ngo', 'donation_date', 'delivery_time','created_on','confirmed','expiration_date','confirmed')
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
admin.site.register(Restaurant,RestaurantAdmin)
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




