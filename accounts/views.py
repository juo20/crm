from django.shortcuts import render, redirect, HttpResponse
from .models import Product, Order, Customer
from . import forms
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
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


@login_required(login_url='login')
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


@login_required(login_url='login')
def products(request):
    products_all = Product.objects.all()

    return render(request, 'accounts/products.html', {'products': products_all})


@login_required(login_url='login')
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


@login_required(login_url='login')
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


@login_required(login_url='login')
def deleteOrder(request, order_id):

    Order.objects.filter(id=order_id).delete()

    return redirect('/')


@login_required(login_url='login')
def createCustomer(request):

    form = forms.CustomerForm()

    if request.method == 'POST':
        form = forms.CustomerForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('/')

    context = {'form': form}

    return render(request, 'accounts/customer_form.html', context)


@login_required(login_url='login')
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


@login_required(login_url='login')
def deleteCustomer(request, cust_id):

    Customer.objects.filter(id=cust_id).delete()

    return redirect('/')


@login_required(login_url='login')
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


@login_required(login_url='login')
def deleteProduct(request, prod_id):

    Product.objects.filter(id=prod_id).delete()

    return redirect('/')


def userLogin(request):
    if request.user.is_authenticated:
        return redirect('/')

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

    context['form'] = form

    return render(request, 'accounts/login.html', context)


def userLogout(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, 'Successfully logged out')
    return redirect('/login')


def register(request):
    if request.user.is_authenticated:
        return redirect('/')

    context = {}

    form = forms.CreateUserForm()

    if request.method == 'POST':
        form = forms.CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Successfully created account')
            return redirect('/login')

    context['form'] = form

    return render(request, 'accounts/register.html', context)
