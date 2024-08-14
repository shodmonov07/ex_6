# customer/admin.py
from django.contrib import admin
from .models import Customer, User


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'address', 'joined', 'is_active')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'birth_of_date', 'is_active', 'is_staff', 'is_superuser')
