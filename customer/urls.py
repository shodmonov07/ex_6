"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from customer import views
from customer.views import customers, add_customer, edit_customer, delete_customer, \
    customer_detail, SendingEmailView, LoginPageView, LogoutView, ExcelExportView, register_page, ActivateAccountView

urlpatterns = [
    path('customers/', customers, name='customers'),
    path('customers/<int:customer_id>/', customer_detail, name='customer_detail'),
    path('add-customer/', add_customer, name='add_customer'),
    path('customer/<int:pk>/delete', delete_customer, name='delete'),
    path('customer/<int:pk>/update', edit_customer, name='edit'),
    path('login_page/', LoginPageView.as_view(), name='login_page'),
    path('logout_page/', LogoutView.as_view(), name='logout_page'),
    path('register_page/', register_page, name='register_page'),
    path('send-email/', SendingEmailView.as_view(), name='sending_email'),
    path('export/customers/', ExcelExportView.as_view(), name='export_customers'),
    path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate'),
]
