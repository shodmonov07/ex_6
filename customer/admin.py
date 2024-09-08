from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Customer, User


@admin.register(Customer)
class CustomerAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'address', 'joined', 'is_active')
    search_fields = ('full_name', 'email', 'phone_number', 'address')
    list_filter = ('is_active', 'address')
    list_per_page = 10
    # prepopulated_fields = {'slug': ('full_name',)}


@admin.register(User)
class UserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_staff', 'is_active')
