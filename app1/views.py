from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Restaurant, NGO
from django.contrib import auth


# Create your views here.
def home(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def loginRegister(request):
    return render(request, 'login-register.html')

def requests_view(request):
    return render(request,'#')

def donate_view(request):
    return render(request,'#')

def charity_view(request):
    return render(request,'#')

def browse_food_view(request):
    return render(request,'#')

def restaurant_view(request):
    return render(request,'#')

def confirmations_view(request):
    return render(request,'#')


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
            # add this if only active users log in ,is_active=False
            user = User.objects.create_user(username=name, password=password )
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
# def login(request):
#     if request.method == 'POST':
#         try:
#             # Check User in DB
#             uname = request.POST['username']
#             pwd = request.POST['password']
#             user_authenticate = auth.authenticate(username=uname, password=pwd)
#             if user_authenticate is not None:
#                 user = User.objects.get(username=uname)
#                 if user.is_staff:
#                     try:
#                         data = Restaurant.objects.get(user=user)
#                         print(data)
#                         print('Patient has been Logged')
#                         auth.login(request, user_authenticate)
#                         return redirect('dashboard', user="P")
#                     except Restaurant.DoesNotExist:
#                         try:
#                             data = NGO.objects.get(user=user)
#                             auth.login(request, user_authenticate)
#                             print('HR has been Logged')
#                             return redirect('dashboard', user="H")
#                         except NGO.DoesNotExist:
#                             return redirect('/')
#                 else:
#                     return render(request, 'login.html', {'error': 'You are not authorized to log in.'})
#             else:
#                 print('Login Failed')
#                 return render(request, 'login.html')
#         except KeyError:
#             return render(request, 'login.html', {'error': 'Invalid username or password'})
#         except User.DoesNotExist:
#             return render(request, 'login.html', {'error': 'User does not exist'})
#     return render(request, 'login.html')
def login(request):
    if request.method == 'POST':
        try:
            # Check User in DB
            uname = request.POST['username']
            pwd = request.POST['password']
            user_authenticate = auth.authenticate(username=uname, password=pwd)
            if user_authenticate is not None:
                user = User.objects.get(username=uname)
                try:
                    data = Restaurant.objects.get(user=user)
                    print(data)
                    print('Restaurant has been Logged')
                    auth.login(request, user_authenticate)
                    return redirect('dashboard', user="R")
                except Restaurant.DoesNotExist:
                    try:
                        data = NGO.objects.get(user=user)
                        auth.login(request, user_authenticate)
                        print('NGO has been Logged')
                        return redirect('dashboard', user="N")
                    except NGO.DoesNotExist:
                        return redirect('/')
            else:
                print('Login Failed')
                return render(request, 'login.html')
        except KeyError:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': 'User does not exist'})
    return render(request, 'login.html')

def dashboard(request, user):
    print(user)
    status = False
    if request.user:
        status = request.user
    if user == "AnonymousUser":
        return redirect('home')

    return render(request, 'index.html', {'user': user, "status": status})


def logout_view(request):
    auth.logout(request)
    print('logout')
    return render(request,'index.html')