from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Restaurant, NGO


# Create your views here.
def home(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def loginRegister(request):
    return render(request, 'login-register.html')


def register(request):
    if request.method == 'POST':
        password = request.POST['password']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        choice = request.POST.get('choice')

        try:
            user = User.objects.get(username=name)
            return render(request, 'login-register.html')
        except User.DoesNotExist:
            user = User.objects.create_user(username=name, password=password)
            print()
            if choice == 'Restaurant':
                restaurant = Restaurant(name=name, contact_email=email, contact_phone=phone, user=user)
                restaurant.save()
                print('Registered as a Restaurant')
            elif choice == 'Charity':
                ngo = NGO(name=name, contact_email=email, contact_phone=phone, user=user)
                ngo.save()
                print('Registered as an NGO')
            else:
                # Handle registration for other roles if needed
                pass
            
            print('Registered Successfully')
            return render(request, 'login-register.html')
    else:
        return render(request, 'login-register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            if Restaurant.objects.filter(user=user).exists():
                print('Restaurant has been logged in')
                # Handle restaurant login logic
                return redirect('restaurant_dashboard')
            elif NGO.objects.filter(user=user).exists():
                print('NGO has been logged in')
                # Handle NGO login logic
                return redirect('ngo_dashboard')
            else:
                # Handle login for other roles if needed
                pass
        else:
            print('Invalid credentials')
            return render(request, 'login.html')
    
    return render(request, 'login.html')
