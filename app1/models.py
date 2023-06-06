import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class FoodItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    expiration_date = models.DateField()
    quantity = models.IntegerField()
    packaging_type = models.CharField(max_length=255)
    food_type = models.CharField(max_length=255)
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE, related_name='food_items',default='')

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    name = models.CharField(max_length=255, default='')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    stock = models.ManyToManyField(FoodItem, related_name='restaurants')
    is_verified = models.BooleanField(default=False)  # Add the is_verified field

    def __str__(self):
        return self.name


class NGO(models.Model):
    name = models.CharField(max_length=255, default='')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    review = models.TextField(blank=True)
    category = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)  # Add the is_verified field

    def __str__(self):
        return self.name


class Donation(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    ngo = models.ForeignKey(NGO, on_delete=models.CASCADE)
    donation_date = models.DateField(default=timezone.now)
    delivery_time = models.CharField(max_length=255, default='')
    posted = models.BooleanField(default=True)  # controlled by restaurant
    confirmed = models.BooleanField(default=True)  # controlled by Charity NGO
    created_on = models.DateTimeField(default=timezone.now)
    food_items_donated = models.ManyToManyField(FoodItem)

    def __str__(self):
        return f"Donation from {self.restaurant} to {self.ngo}"


class RestRequest(models.Model):
    ngo = models.ForeignKey(NGO, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity_requested = models.IntegerField()  # quantity by person
    confirmed = models.BooleanField(default=True)  # controlled by Charity NGO
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE)

    def __str__(self):
        return f"RestRequest - NGO: {self.ngo.name}, Food Item: {self.food_item.name}, Quantity Requested: {self.quantity_requested}, Confirmed: {self.confirmed}, Donation: {self.donation}"
