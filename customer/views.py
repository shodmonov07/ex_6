from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.db.models import Q
from django.shortcuts import render, redirect
from customer.forms import CustomerModelForm, RegisterForm, LoginForm
from customer.models import Customer
from django.contrib.auth.decorators import permission_required, login_required


# Create your views here.

def customers(request):
    search_query = request.GET.get('search')
    if search_query:
        customer_list = Customer.objects.filter(
            Q(full_name__icontains=search_query) | Q(address__icontains=search_query))
    else:
        customer_list = Customer.objects.all()
    context = {
        'customer_list': customer_list,
    }
    return render(request, 'customer/customer-list.html', context)


@login_required
@permission_required('customer.view_customer', raise_exception=True)
def add_customer(request):
    form = CustomerModelForm()
    if request.method == 'POST':
        form = CustomerModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('customers')

    context = {
        'form': form,
    }

    return render(request, 'customer/add-customer.html', context)


def delete_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    if customer:
        customer.delete()
        messages.add_message(
            request,
            messages.SUCCESS,
            'Customer successfully deleted'
        )
        return redirect('customers')


@permission_required('customer.can_change_customer', raise_exception=True)
def edit_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    form = CustomerModelForm(instance=customer)
    if request.method == 'POST':
        form = CustomerModelForm(instance=customer, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()

            return redirect('customers')
    context = {
        'form': form,
    }
    return render(request, 'customer/update-customer.html', context)


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<AUTH>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('customers')
            else:
                messages.error(request,
                               'Invalid username or password')
                # sending message
                pass


    else:
        form = LoginForm()
    return render(request, 'customer/customer-list.html', {'form': form})


def logout_page(request):
    if request.method == 'POST':
        logout(request)
        return redirect('customers')


def register_page(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('customers')
    else:
        form = RegisterForm()

    context = {
        'form': form
    }

    return render(request, 'auth/register.html', context)
