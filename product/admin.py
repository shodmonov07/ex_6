from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from product.models import Product, Attribute, AttributeValue, ProductAttribute


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'available', 'created', 'updated')
    search_fields = ('name', 'description')
    list_filter = ('available', 'created', 'updated')
    list_editable = ('price', 'stock', 'available')
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 10


@admin.register(Attribute)
class AttributeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    list_filter = ('name',)
    list_per_page = 10


@admin.register(AttributeValue)
class AttributeValueAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('attribute', 'value')
    search_fields = ('value',)
    list_filter = ('attribute',)
    list_per_page = 10


@admin.register(ProductAttribute)
class ProductAttributeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('product', 'attribute', 'value')
    search_fields = ('product__name', 'attribute__name', 'value__value')
    list_filter = ('product', 'attribute', 'value')
    list_per_page = 10
