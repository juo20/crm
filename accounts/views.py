from django.shortcuts import render, redirect, HttpResponse
from .models import Product, Order, Customer
from . import forms
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


# Create your views here.
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_orders = orders.count()
    total_customers = customers.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    last_five_orders = orders.order_by('-id')[:5]

    context = {
        'orders': last_five_orders,
        'customers': customers,
        'total_orders': total_orders,
        'total_customers': total_customers,
        'delivered': delivered,
        'pending': pending
    }

    return render(request, 'accounts/home.html', context)


def customers(request, cust_id):
    customer = Customer.objects.get(id=cust_id)
    orders = customer.order_set.all()
    total_orders = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {
        'customer': customer,
        'orders': orders,
        'total_orders': total_orders,
        'myFilter': myFilter
    }

    return render(request, 'accounts/customers.html', context)


def products(request):
    products_all = Product.objects.all()

    return render(request, 'accounts/products.html', {'products': products_all})


def createOrder(request, cust_id):

    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), max_num=3)
    customer = Customer.objects.get(id=cust_id)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)

    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()

            return redirect('/')

    context = {'formset': formset, 'customer': customer}

    return render(request, 'accounts/order_form.html', context)


def updateOrder(request, order_id):

    order = Order.objects.get(id=order_id)
    form = forms.OrderForm(instance=order)

    if request.method == 'POST':
        form = forms.OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()

            return redirect('/')

    context = {'form': form}

    return render(request, 'accounts/update_order_form.html', context)


def deleteOrder(request, order_id):

    Order.objects.filter(id=order_id).delete()

    return redirect('/')


def createCustomer(request):

    form = forms.CustomerForm()

    if request.method == 'POST':
        form = forms.CustomerForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('/')

    context = {'form': form}

    return render(request, 'accounts/customer_form.html', context)


def updateCustomer(request, cust_id):

    customer = Customer.objects.get(id=cust_id)
    form = forms.CustomerForm(instance=customer)

    if request.method == 'POST':
        form = forms.CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()

            return redirect('/')

    context = {'form': form}

    return render(request, 'accounts/customer_form.html', context)


def deleteCustomer(request, cust_id):

    Customer.objects.filter(id=cust_id).delete()

    return redirect('/')


def updateProduct(request, prod_id):

    product = Product.objects.get(id=prod_id)
    form = forms.ProductForm(instance=product)

    if request.method == 'POST':
        form = forms.ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()

            return redirect('/')

    context = {'form': form}

    return render(request, 'accounts/update_product_form.html', context)


def deleteProduct(request, prod_id):

    Product.objects.filter(id=prod_id).delete()

    return redirect('/')


def userLogin(request):

    context = {}

    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(None, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')
            return HttpResponse("Failed login", status=401)
        else:
            return HttpResponse("Invalid Form", status=403)
    context['form'] = form

    return render(request, 'accounts/login.html', context)


def register(request):
    context = {}

    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = User.objects.create_user(username, username, password)
            user.save()
            return redirect('/')

    context['form'] = form

    return render(request, 'accounts/register.html', context)