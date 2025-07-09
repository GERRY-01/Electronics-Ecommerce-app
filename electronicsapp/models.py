from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Registration(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10)
    
class Adminregistration(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100)
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    categories = (
        ('phones', 'phones'),
        ('laptops', 'laptops'),
        ('television', 'television'),
        ('computers', 'computers'),
        ('cables', 'cables'),
        ) 
    category = models.CharField(max_length=100, choices=categories)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
   
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    time = models.DateTimeField(auto_now_add=True)