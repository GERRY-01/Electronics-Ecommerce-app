import base64
from datetime import datetime
from urllib import response
from django.conf import settings
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
import requests
from .models import Cart, Product, Registration,Adminregistration,Contact
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib.auth.decorators import login_required
from requests.auth import HTTPBasicAuth
# Create your views here.

def home(request):
    cart_count = 0
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        cart_count = sum(item.quantity for item in cart_items)
    products = Product.objects.all()
    
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == "contact_form":
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            contact = Contact(name=name, email=email, subject=subject, message=message)
            contact.save() 
            messages.success(request, 'Message sent successfully.')
            return redirect('home')       
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
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to add items to the cart.')
        return redirect('home')
    product = Product.objects.get(id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, 'Item added to cart successfully.')
    return redirect('home')

def cart(request):
    total_price = sum(item.product.price * item.quantity for item in Cart.objects.filter(user=request.user))
    cart_count = 0
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        cart_count = sum(item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'cart_count': cart_count, 'total_price': total_price})

def update_cart(request, cart_item_id):
    if request.method == 'POST':
        try:
            cart_item = Cart.objects.get(id=cart_item_id, user=request.user)
            new_quantity = int(request.POST.get('quantity', 1))
            if 1 <= new_quantity <= cart_item.product.stock:
                cart_item.quantity = new_quantity
                cart_item.save()
        except (Cart.DoesNotExist, ValueError):
            pass
    return redirect('cart')

def remove_from_cart(request, cart_item_id):
    try:
        cart_item = Cart.objects.get(id=cart_item_id, user=request.user)
        cart_item.delete()
    except Cart.DoesNotExist:
        pass
    return redirect('cart')

def get_access_token(request):
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET
    api_URL = settings.MPESA_API_URL
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    return r.json()['access_token']

def lipa_na_mpesa(request):
    if request.method == 'POST':
        phone = request.POST.get("phone")
        amount = float(request.POST.get("amount"))
        
        if phone.startswith("07") and len(phone) == 10:
            phone = "254" + phone[1:]
        elif phone.startswith("+254") and len(phone) == 13:
            phone = phone[1:]
        elif phone.startswith("254") and len(phone) == 12:
            phone = phone
        else:
            messages.error(request,"Invalid phone number")
            return redirect("home")
        
        phone = phone.strip().replace(" ", "")

        
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        data_to_encode = f"{settings.MPESA_SHORTCODE}{settings.MPESA_PASSKEY}{timestamp}"
        password = base64.b64encode(data_to_encode.encode()).decode()
        
        access_token = get_access_token(request)
        base_url = settings.LIPA_NA_MPESA_URL
        headers = {"Authorization": "Bearer %s" % access_token}
        payload = {
            "BusinessShortCode": settings.MPESA_SHORTCODE,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": settings.MPESA_SHORTCODE,
            "PhoneNumber": phone,
            "CallBackURL": "https://mydomain.com/payload",
            "AccountReference": "Car Booking",
            "TransactionDesc": "Payment of Electronics"
        }
        
        res = requests.post(base_url, json=payload, headers=headers)
        res_data = res.json()
    
        if res_data.get("ResponseCode") == "0":
            messages.success(request, "Payment request sent. Check your phone.")
        else:
            messages.error(request, res_data.get("errorMessage", "Something went wrong. Try again."))

        return redirect("home")
    return render(request,'home.html')

def contact_messages(request):
    contact_data = Contact.objects.all()
    return render(request, 'contact_messages.html',{'contact_data':contact_data})
    
