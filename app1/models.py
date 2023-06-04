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
    
    def __str__(self):
        return f"Food Item: {self.name}, Description: {self.description}, Expiration Date: {self.expiration_date}, Quantity: {self.quantity}"


class Restaurant(models.Model):
    name = models.CharField(max_length=255,default='')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    stock = models.ManyToManyField(FoodItem, related_name='restaurants')
    
    def __str__(self):
        return f"Restaurant: {self.name}, Location: {self.location}, Email: {self.contact_email}, Phone: {self.contact_phone}"


class NGO(models.Model):
    name = models.CharField(max_length=255,default='')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    review = models.TextField()
    category = models.CharField(max_length=255)
    
    def __str__(self):
        return f"NGO: {self.name}, Location: {self.location}, Email: {self.contact_email}, Phone: {self.contact_phone}, Review: {self.review}, Category: {self.category}"


class Donation(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    ngo = models.ForeignKey(NGO, on_delete=models.CASCADE)
    food_items_donated = models.CharField(max_length=255,default='') 
    donation_date = models.DateField(default=timezone.now)
    delivery_time = models.CharField(max_length=255, default='')
    posted = models.BooleanField(default=True) #controlled by restaurant
    confirmed = models.BooleanField(default=True) #controlled by Charity NGO
    created_on = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Donation - Restaurant: {self.restaurant.name}, NGO: {self.ngo.name}, Donation Date: {self.donation_date}, Delivery Time: {self.delivery_time}, Posted: {self.posted}, Confirmed: {self.confirmed}, Created On: {self.created_on}"


class Rest_Request(models.Model):
    ngo = models.ForeignKey(NGO, on_delete=models.CASCADE)
    food_items_donated = models.CharField(max_length=255,default='') 
    quatityRequested = models.IntegerField() # quatity by person
    confirmed = models.BooleanField(default=True) #controlled by Charity NGO
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Rest_Request - NGO: {self.ngo.name}, Quantity Requested: {self.quatityRequested}, Confirmed: {self.confirmed}, Donation: {self.donation}"
