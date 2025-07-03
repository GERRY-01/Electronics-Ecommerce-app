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
    path('add_to_cart/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    path('update_cart/<int:cart_item_id>', views.update_cart, name='update_cart'),
    path('remove_from_cart/<int:cart_item_id>', views.remove_from_cart, name='remove_from_cart'),
    path('cart',views.cart,name='cart'),
]