from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView, UpdateView, DetailView, CreateView, ListView

from product.forms import ProductModelForm
from product.models import Product


# def product_list(request):
#     page = request.GET.get('page', '')
#     products = Product.objects.all().order_by('-id')
#     paginator = Paginator(products, 2)
#     try:
#         page_obj = paginator.page(page)
#     except PageNotAnInteger:
#         page_obj = paginator.page(1)
#     except EmptyPage:
#         page_obj = paginator.page(paginator.num_pages)
#
#     context = {
#         'page_obj': page_obj
#     }
#     return render(request, 'product/product-list.html', context)


# class ProductListView(View):
#     def get(self, request):
#         products = Product.objects.all().order_by('-id')
#         paginator = Paginator(products, 3)  # Har bir sahifada 3 ta mahsulot
#
#         page_number = request.GET.get('page')
#
#         try:
#             page_obj = paginator.page(page_number)
#         except PageNotAnInteger:
#             page_obj = paginator.page(1)
#         except EmptyPage:
#             page_obj = paginator.page(paginator.num_pages)
#
#         context = {
#             'page_obj': page_obj
#         }
#         return render(request, 'product/product-list.html', context)


class ProductListView(ListView):
    model = Product
    template_name = 'product/product-list.html'
    context_object_name = 'products'
    paginate_by = 3  # Har bir sahifada 10 ta mahsulot


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/product-details.html'
    context_object_name = 'product'


# Yangi mahsulot yaratish uchun CreateView
class ProductCreateView(CreateView):
    model = Product
    template_name = 'product/product-add.html'
    fields = ['name', 'description', 'price', 'quantity', 'discount', 'rating', 'image']
    success_url = reverse_lazy('ProductListView')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Product successfully added')
        return response


class EditProductView(PermissionRequiredMixin, UpdateView):
    model = Product
    template_name = 'product/product-update.html'
    fields = ['name', 'description', 'price', 'quantity', 'discount', 'rating', 'image']
    success_url = reverse_lazy('ProductListView')
    permission_required = 'product.can_change_product'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Product successfully updated')
        return response


# # Mahsulotni o'chirish uchun DeleteView
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product/product-delete.html'
    success_url = reverse_lazy('ProductListView')
