from django.urls import path
from .views import *




urlpatterns = [
    path('', home, name='home'),
    path('contact/',contact,name='contact'),
    path('login-register/',loginRegister,name='loginRegister'),
    path('about/',about,name='about'),
    path('login/', login, name='login'),
    path('register/',register, name='register'),
    path('dashboard/<str:user>/', dashboard, name='dashboard'),
    path('requests', requests_view, name='requests'),
    path('donate', donate_view, name='donate'),
    path('charity', charity_view, name='charity'),
    path('browse-food', browse_food_view, name='browse_food'),
    path('restaurant', restaurant_view, name='restaurant'),
    path('confirmations', confirmations_view, name='confirmations'),
    path('logout',logout_view, name='logout'),

]