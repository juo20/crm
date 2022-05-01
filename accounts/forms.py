from django.forms import ModelForm
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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


class CreateUserForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
