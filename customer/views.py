from django.contrib import messages
from django.contrib.auth import logout, login, authenticate, get_user_model
from django.contrib.sites.shortcuts import get_current_site
# from django.contrib.auth.views import LoginView
from django.core.mail import send_mail, EmailMessage
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import View
from openpyxl.workbook import Workbook

from config.settings import EMAIL_DEFAULT_SENDER
from customer.forms import CustomerModelForm, RegisterForm, LoginForm, SendingEmailForm
from customer.models import Customer, User
from django.contrib.auth.decorators import permission_required

from customer.tokens import account_activation_token


# Create your views here.

def customers(request):
    search_query = request.GET.get('search')
    if search_query:
        customer_list = Customer.objects.filter(
            Q(full_name__icontains=search_query) | Q(address__icontains=search_query) |
            Q(email__icontains=search_query))
    else:
        customer_list = Customer.objects.all()
    context = {
        'customer_list': customer_list,
    }
    return render(request, 'customer/customer-list.html', context)


def customer_detail(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    return render(request, 'customer/customer-detail.html', {'customer': customer})


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


# def login_page(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             email: str = form.cleaned_data['email']
#             password: str = form.cleaned_data['password']
#             user = authenticate(request, email=email, password=password)
#             if user:
#                 login(request, user)
#                 return redirect('customers')
#             else:
#                 messages.error(request, 'Invalid Username or Password')
#     else:
#         form = LoginForm()
#     return render(request, 'auth/login.html', {'form': form})


class LoginPageView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, 'auth/login.html', {'form': form})

    def post(self, request, *args, **kwargs):
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
        return render(request, 'auth/login.html', {'form': form})


def register_page(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('auth/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            email = EmailMessage(
                'Activate your account',
                message,
                EMAIL_DEFAULT_SENDER,
                [user.email],

            )
            email.content_subtype = 'html'
            email.send()

            return HttpResponse('<h1>Please confirm your email address to complete the registration</h1>')
            # login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            # return redirect('customers')
    else:
        form = RegisterForm()
    context = {'form': form}
    return render(request, 'auth/register.html', context)


# class RegisterView(View):
#     def get(self, request, *args, **kwargs):
#         form = RegisterForm()
#         return render(request, 'auth/register.html', {'form': form})
#
#     def post(self, request, *args, **kwargs):
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.save()
#             send_mail(
#                 'User Successfully Registered',
#                 'Test body',
#                 EMAIL_DEFAULT_SENDER,
#                 [user.email],
#                 fail_silently=False
#             )
#
#             # Authenticate the user and set the backend
#             user = authenticate(request, email=user.email, password=request.POST['password'])
#             if user:
#                 user.backend = 'django.contrib.auth.backends.ModelBackend'  # or your specific backend
#                 login(request, user)
#                 return redirect('customers')
#             else:
#                 messages.error(request, 'Authentication failed')
#
#         return render(request, 'auth/register.html', {'form': form})


class LogoutView(View):
    def post(self, request, *args, **kwargs):
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


class ExcelExportView(View):
    def get(self, request, *args, **kwargs):
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = 'Customers'

        sheet.append(['ID', 'Name', 'Email', 'Phone'])

        customers = Customer.objects.all()
        for customer in customers:
            sheet.append([customer.id, customer.name, customer.email, customer.phone])

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=customers.xlsx'

        workbook.save(response)
        return response


def active(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = Users.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Users.DoesNotExist):
        user = None
    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


Users = get_user_model()


class ActivateAccountView(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_bytes(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            # Email tasdiqlangandan keyin 'customers' sahifasiga yo'naltirish
            return redirect('customers')
        else:
            return HttpResponse('Activation link is invalid!')