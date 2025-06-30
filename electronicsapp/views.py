from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Registration

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
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        
        registration = Registration(user=user, phone=phone)
        registration.save()
        
        messages.success(request, 'Registration successful. Now login')
        return render(request, 'Login.html')
    return render(request,'Signup.html')

def login(request):
    return render(request,'Login.html')