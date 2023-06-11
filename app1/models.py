from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, timedelta


class Donation(models.Model):
    name = models.CharField(max_length=255, editable=False)
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE, related_name='donations')
    ngo = models.ForeignKey('NGO', on_delete=models.CASCADE, related_name='donations_received')
    donation_date = models.DateField(default=timezone.now)
    delivery_time = models.TimeField(default=timezone.now)
    created_on = models.DateTimeField(default=timezone.now)
    expiration_date = models.DateField(default=date.today() + timedelta(days=3))
    confirmed = models.BooleanField(default=False)
    requested = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f"{self.restaurant.name}_{timezone.now().strftime('%Y%m%d')}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='')
    location = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class NGO(models.Model):
    name = models.CharField(max_length=255, default='')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    capacity = models.IntegerField(default=0)
    review = models.TextField(blank=True)
    category = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class DonationRequest(models.Model):
    donation = models.ForeignKey('Donation', on_delete=models.CASCADE, related_name='donation_requests')
    ngo = models.ForeignKey('NGO', on_delete=models.CASCADE, related_name='donation_requests_received')
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Donation Request - NGO: {self.ngo.name}, Donation: {self.donation.name}"
