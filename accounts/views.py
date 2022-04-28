from django.shortcuts import render, redirect
from .models import Product, Order, Customer
from . import forms


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

    context = {'customer': customer, 'orders': orders, 'total_orders': total_orders}
    return render(request, 'accounts/customers.html', context)


def products(request):
    products_all = Product.objects.all()

    return render(request, 'accounts/products.html', {'products': products_all})


def createOrder(request):

    form = forms.OrderForm()

    if request.method == 'POST':
        form = forms.OrderForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('/')

    context = {'form': form}

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