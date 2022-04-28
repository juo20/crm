from django.forms import ModelForm
from .models import *
from django import forms


class OrderForm(ModelForm):

    class Meta:
        model = Order
        fields = ['product', 'status', 'customer']


class CustomerForm(ModelForm):

    class Meta:
        model = Customer
        fields = '__all__'


class ProductForm(ModelForm):

    class Meta:
        model = Product
        fields = '__all__'
