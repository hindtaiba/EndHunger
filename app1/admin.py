from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

class DonationAdmin(admin.ModelAdmin):
    list_display = ('restaurant','ngo','donation_date','delivery_time','posted','confirmed')
    readonly_fields = ( )

    def get_queryset(self, request):
        # Only display appointments for the current user
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            # Superusers can see all appointments
            return qs
        elif hasattr(request.user, 'ngo'):
            return qs.filter(doctor=request.user.ngo)
        elif hasattr(request.user, 'restaurant'):
            return qs.filter(nurse=request.user.restaurant)
        else:
            # Non-doctor users won't see any appointments
            return qs.none()

    def get_readonly_fields(self, request, obj=None):
        if  hasattr(request.user, 'ngo'):  # Editing an existing user
            return self.readonly_fields + ('confirmed',)
        if  hasattr(request.user, 'restaurant'):  # Editing an existing user
            return self.readonly_fields + ('donation_date','delivery_time')

        return self.readonly_fields

admin.site.register(Donation,DonationAdmin)

admin.site.register(NGO)
admin.site.register(Restaurant)

admin.site.register(FoodItem)

