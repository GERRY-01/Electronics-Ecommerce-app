from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('signup',views.signup,name='signup'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('adminsignup',views.adminsignup,name='adminsignup'),
    path('adminlogin',views.adminlogin,name='adminlogin'),
    path('adminhome',views.adminhome,name='adminhome'),
    path('delete/<int:id>',views.delete,name='delete'),
    path('editproduct/<int:id>',views.editproduct,name='editproduct'),
    path('cart',views.cart,name='cart'),
]