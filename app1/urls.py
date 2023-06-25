from django.urls import path
from .views import *
from django.contrib.auth.views import PasswordResetConfirmView




urlpatterns = [
    path('', home, name='home'),
    path('contact/', contact, name='contact'),
    path('login-register/',loginRegister,name='loginRegister'),
    path('about/',about,name='about'),
    path('login/', login, name='login'),
    path('register/',register, name='register'),
    path('dashboard/<str:user>/', dashboard, name='dashboard'),
    path('donate/', add_donation, name='donate'),
    path('submit_donation/', submit_donation, name='submit_donation'),
    path('charity/', charity_view, name='charity'),
    path('browse_donations/', view_donations, name='browse_donations'),
    path('restaurant/', restaurant_view, name='restaurant'),
    path('requestsR/', requestsR_view, name='confirmations'),
    path('requestsN/', requestsN_view, name='confirmations'),
    path('logout/',logout_view, name='logout'),
    path('verify_email/<str:uidb64>/<str:token>/', verify_email, name='verify_email'),
    path('password_reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('password_reset/confirm/<str:uidb64>/<str:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/complete/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('donation/request/<str:donation_name>/',request_donation, name='request_donation'),
    path('confirm_donation/<int:donation_id>/', confirm_donation, name='confirm_donation'),
    path('update-profile/',update_profile, name='update_profile'),
    path('restaurant/<int:restaurant_id>/', restaurant_detail, name='restaurant_detail'),

]