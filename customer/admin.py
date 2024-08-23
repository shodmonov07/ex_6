# customer/admin.py
from django.contrib import admin
from .models import Customer, User


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'address', 'joined', 'is_active')
    search_fields = ('full_name', 'email', 'phone_number', 'address')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = ('email', 'date_of_birth')
    search_fields = ('email',)
