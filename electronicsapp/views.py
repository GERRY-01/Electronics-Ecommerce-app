from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Cart, Product, Registration,Adminregistration
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
# Create your views here.

def home(request):
    cart_count = 0
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        cart_count = cart_items.count()
    products = Product.objects.all()
    return render(request,'home.html',{'products':products,'cart_count':cart_count})

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
    is_admin = request.user.is_superuser
    auth_logout(request)
    if is_admin:
        return redirect('adminlogin')
    return redirect('login')

def adminsignup(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'adminsignup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'adminsignup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'adminsignup.html')

        user = User.objects.create_user(username=username, email=email, password=password,is_staff=True,is_superuser=True)
        user.save()

        adminregistration = Adminregistration(user=user, fullname=fullname)
        adminregistration.save()

        messages.success(request, 'Admin registration successful. Now login')
        return redirect('adminlogin')
    return render(request,'adminsignup.html')

def adminlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('adminhome')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'adminlogin.html')
    return render(request,'adminlogin.html')

def adminhome(request):
    if request.user.is_superuser == True:
        if request.method == 'POST':
            productname = request.POST.get('productname')
            category = request.POST.get('category')
            price = request.POST.get('price')
            stock = request.POST.get('stock')
            image = request.FILES.get('image')

            product = Product(name=productname, category=category, price=price, stock=stock, image=image)
            product.save()
        
            return redirect('adminhome')
        
        products = Product.objects.all()
        
    else:
        messages.error(request, 'You are not authorized to access this page!!')
        return redirect('adminlogin')
    return render(request,'adminhome.html',{'products':products})

def delete(request,id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect('adminhome')

def editproduct(request,id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        product.name = request.POST.get('productname')
        product.category = request.POST.get('category')
        product.price = request.POST.get('price')
        product.stock = request.POST.get('stock')
        
        if request.FILES.get('image'):
            product.image = request.FILES.get('image')
        product.save()
        return redirect('adminhome')
    return render(request,'editproduct.html',{'product':product})


def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('home')

def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    return render(request, 'cart.html', {'cart_items': cart_items})