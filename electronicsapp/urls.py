from django.urls import path
from django.contrib.auth import views as auth_views
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
    
    #auth paths
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('lipa_na_mpesa', views.lipa_na_mpesa, name='lipa_na_mpesa'),
    path('contact_messages', views.contact_messages, name='contact_messages'),
   
]