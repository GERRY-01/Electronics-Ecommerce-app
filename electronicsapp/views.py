from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Registration
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
# Create your views here.

def home(request):
    return render(request,'home.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'Signup.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'Signup.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'Signup.html')
        
        if len(phone) != 10:
            messages.error(request, 'Phone number should be 10 digits.')
            return render(request, 'Signup.html')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        
        registration = Registration(user=user, phone=phone)
        registration.save()
        
        messages.success(request, 'Registration successful. Now login')
        return redirect('login')
    return render(request,'Signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'Login.html')
    return render(request,'Login.html')

def logout(request):
    auth_logout(request)
    return redirect('login')