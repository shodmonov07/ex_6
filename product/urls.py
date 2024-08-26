from django.urls import path

from product.views import ProductListView, ProductDetailView, ProductCreateView, EditProductView, ProductDeleteView, \
    ProductExcelExportView

urlpatterns = [
    path('product_list', ProductListView.as_view(), name='ProductListView'),
    path('product_details/<int:pk>/', ProductDetailView.as_view(), name='ProductDetailView'),
    path('product_add', ProductCreateView.as_view(), name='ProductCreateView'),
    path('product_update/<int:pk>/', EditProductView.as_view(), name='edit_product'),
    path('product_delete/<int:pk>/', ProductDeleteView.as_view(), name='ProductDeleteView'),
    path('export/products/', ProductExcelExportView.as_view(), name='export_products'),
]
