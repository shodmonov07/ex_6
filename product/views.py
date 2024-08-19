from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.shortcuts import render

from product.models import Product


def product_list(request):
    page = request.GET.get('page', '')
    products = Product.objects.all().order_by('-id')
    paginator = Paginator(products, 2)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'page_obj': page_obj
    }
    return render(request, 'product/product-list.html', context)