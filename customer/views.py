from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View, FormView

from config.settings import EMAIL_DEFAULT_SENDER
from customer.forms import CustomerModelForm, RegisterForm, LoginForm, SendingEmailForm
from customer.models import Customer
from django.contrib.auth.decorators import permission_required, login_required


# Create your views here.

def customers(request):
    search_query = request.GET.get('search')
    if search_query:
        customer_list = Customer.objects.filter(
            Q(full_name__icontains=search_query) | Q(address__icontains=search_query) | Q(email__icontains=search_query))
    else:
        customer_list = Customer.objects.all()
    context = {
        'customer_list': customer_list,
    }
    return render(request, 'customer/customer-list.html', context)


def customer_detail(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    return render(request, 'customer/customer-detail.html', {'customer': customer})


@login_required
@permission_required('customer.view_customer', raise_exception=True)
def add_customer(request):
    customer = Customer.objects.all()
    form = CustomerModelForm()
    if request.method == 'POST':
        form = CustomerModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('customers')

    context = {
        'form': form,
        'customers': customer,
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
            email: str = form.cleaned_data['email']
            password: str = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect('customers')
            else:
                messages.error(request, 'Invalid Username or Password')
    else:
        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form})


# class LoginPage(LoginView):
#     redirect_authenticated_user = True
#     form_class = AuthenticationForm
#     template_name = 'auth/login.html'
#
#     def get_success_url(self):
#         return reverse_lazy('customers')
#
#     def form_invalid(self, form):
#         messages.error(self.request, 'Invalid email or password')
#         return self.render_to_response(self.get_context_data(form=form))


def register_page(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            send_mail(
                'User Succesfully Registered',
                'Test body',
                EMAIL_DEFAULT_SENDER,
                [user.email],
                fail_silently=False

            )
            login(request, user)
            return redirect('customers')
    else:
        form = RegisterForm()
    context = {'form': form}
    return render(request, 'auth/register.html', context)


# class RegisterPage(FormView):
#     template_name = 'auth/register.html'
#     form_class = RegisterForm
#     success_url = reverse_lazy('customers')
#
#     def form_valid(self, form):
#         user = form.save(commit=False)
#         user.save()
#         send_mail(
#             'User Succesfully Registered',
#             'Test body',
#             EMAIL_DEFAULT_SENDER,
#             [user.email],
#             fail_silently=False
#
#         )
#         login(self.request, user)
#         return super().form_valid(form)


def logout_page(request):
    if request.method == 'POST':
        logout(request)
        return redirect('customers')


class SendingEmailView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sent = False

    def get(self, request, *args, **kwargs):
        context = {
            'form': SendingEmailForm(),
            'sent': self.sent
        }
        return render(request, 'send-email.html', context)

    def post(self, request, *args, **kwargs):
        form = SendingEmailForm(request.POST)
        if form.is_valid():
            send_mail(
                form.cleaned_data['subject'],
                form.cleaned_data['message'],
                EMAIL_DEFAULT_SENDER,
                form.cleaned_data['recipient_list'],
                fail_silently=False
            )
            self.sent = True
        return render(request, 'send-email.html', {'form': form, 'sent': self.sent})
