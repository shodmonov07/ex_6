from django.urls import path

from product.views import product_list

urlpatterns = [
    path('/product_list/', product_list, name='product_list'),
]
