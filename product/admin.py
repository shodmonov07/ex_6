from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from product.models import Product, Attribute, AttributeValue, ProductAttribute


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity',)
    search_fields = ('name', 'description')
    list_filter = ('quantity',)
    list_editable = ('price', 'quantity')
    # prepopulated_fields = {'slug': ('name',)}
    list_per_page = 10


@admin.register(Attribute)
class AttributeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('key_name',)
    search_fields = ('key_name',)
    list_filter = ('key_name',)
    list_per_page = 10


@admin.register(AttributeValue)
class AttributeValueAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('value_name',)
    search_fields = ('value_name',)
    list_filter = ('value_name',)
    list_per_page = 10


@admin.register(ProductAttribute)
class ProductAttributeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('product', 'attribute', 'attribute_value')
    search_fields = ('product', 'attribute', 'attribute_value')
    search_fields = ('product',)
    list_filter = ('product', 'attribute', 'attribute_value')
    list_per_page = 10
