from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class FoodItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    expiration_date = models.DateField()
    quantity = models.IntegerField()
    packaging_type = models.CharField(max_length=255)
    food_type = models.CharField(max_length=255)

# class Staff(User):
   

class Restaurant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    delivery_time = models.CharField(max_length=255)
    stock = models.ManyToManyField(FoodItem, related_name='restaurants')

class NGO(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    accepted_food_items = models.ManyToManyField(FoodItem, related_name='ngos')
    received_donations = models.ForeignKey('Donation', on_delete=models.CASCADE, null=True, blank=True,related_name='ngo_donations')
    review = models.TextField()
    delivery_time = models.CharField(max_length=255)
    category = models.CharField(max_length=255)

class Donation(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    ngo = models.ForeignKey(NGO, on_delete=models.CASCADE)
    food_items_donated = models.ManyToManyField(FoodItem)
    donation_date = models.DateField()
