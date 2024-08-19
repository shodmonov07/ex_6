# customer/admin.py
from django.contrib import admin
from .models import Customer, User


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'address', 'joined', 'is_active')
<<<<<<< HEAD
    search_fields = ('full_name', 'email', 'phone_number', 'address')
=======
>>>>>>> 33a6095feed2a8e74b640de926d519c52ffc0c40


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
<<<<<<< HEAD
    list_display = ('email', 'date_of_birth')
    search_fields = ('email',)


=======
    list_display = ('email', 'username', 'birth_of_date', 'is_active', 'is_staff', 'is_superuser')
>>>>>>> 33a6095feed2a8e74b640de926d519c52ffc0c40
