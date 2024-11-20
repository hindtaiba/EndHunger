from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, timedelta


class Donation(models.Model):
    name = models.CharField(max_length=255, editable=False, unique=True)
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE, related_name='donations')
    ngo = models.ForeignKey('NGO', on_delete=models.CASCADE, related_name='donations_received', null= True)
    donation_date = models.DateField(default=date.today, null=True)
    delivery_time = models.TimeField(default=timezone.now)
    created_on = models.DateTimeField(default=timezone.now)
    expiration_date = models.CharField(max_length=255, default='')
    confirmed = models.BooleanField(default=False)
    requested = models.BooleanField(default=False)
    transportation = models.CharField(max_length=255,default='')
    packaging = models.CharField(max_length=255,default='')
    quantity = models.CharField(max_length=255,default='')
    food_condition = models.CharField(max_length=100, default='')
    
    def get_quantity_category(self):
        if self.quantity.isdigit():
            quantity_value = int(self.quantity)
            if quantity_value < 50:
                return "less than 50"
            elif 50 <= quantity_value < 100:
                return "50-100"
            elif 100 <= quantity_value < 200:
                return "100-200"
            elif 200 <= quantity_value < 500:
                return "200-500"
            else:
                return "more than 500"
        return ""

    def save(self, *args, **kwargs):
        if not self.name:
            base_name = f"{self.restaurant.name}_"
            name_exists = True
            unique_id = 1
            while name_exists:
                name_to_check = f"{base_name}{unique_id}"
                name_exists = Donation.objects.filter(name=name_to_check).exists()
                if not name_exists:
                    self.name = name_to_check
                else:
                    unique_id += 1
        if self.confirmed and not self.donation_date:  # If confirmed and donation_date not set
            self.donation_date = timezone.now().date()  # Set donation_date to current date
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='')
    location = models.CharField(max_length=255)
    contact_email = models.EmailField(null=False)
    contact_phone = models.CharField(max_length=20, null= False)
    is_verified = models.BooleanField(default=False)
    cuisine_type= models.CharField(max_length=255, default='')
    profile_picture = models.ImageField(upload_to='restaurant_profiles', blank=True, null=True)
    description = models.CharField(max_length=255, default='')


    def __str__(self):
        return self.name


class NGO(models.Model):
    name = models.CharField(max_length=255, default='')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    capacity =  models.CharField(max_length=20,null=True)
    is_verified = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='ngo_profiles', blank=True, null=True)
    description = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.name

