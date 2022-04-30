from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('customers/<str:cust_id>/', views.customers, name='customers'),
    path('products/', views.products, name='products'),
    path('create_order/<str:cust_id>/', views.createOrder, name='create_order'),
    path('update_order/<str:order_id>/', views.updateOrder, name='update_order'),
    path('delete_order/<str:order_id>/', views.deleteOrder, name='delete_order'),
    path('create_customer/', views.createCustomer, name='create_customer'),
    path('update_customer/<str:cust_id>/', views.updateCustomer, name='update_customer'),
    path('delete_customer/<str:cust_id>/', views.deleteCustomer, name='delete_customer'),
    path('update_product/<str:prod_id>/', views.updateProduct, name='update_product'),
    path('delete_product/<str:prod_id>/', views.deleteProduct, name='delete_product'),
    path('login/', views.userLogin, name='login'),
    path('register/', views.register, name='register'),
]
