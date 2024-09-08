from django.shortcuts import render
from django.db.models import Min, Max, Avg, Count, Sum

from app.models import Author, Book


# Create your views here.

#
# def index(request):
#     # authors = {'authors_count':3}
#     authors = Author.objects.all().aggregate(authors_count=Count('id'))
#     count = authors.get('authors_count')
#     return render(request, 'app/index.html', {'count': count})
#
#
# def book_list(request):
#     books = Book.objects.all().annotate(min_price=Max('price')).filter(min_price__gt = 5000
#     ).order_by('-min_price').aggregate(avg_book_price=Avg('min_price'))
#     print(books)
#
#     return render(request, 'app/index.html', {'books': books})


def authors_book_count(request):
    authors = Author.objects.annotate(book_count=Count('books'))
    return render(request, 'app/book_count.html', {'authors': authors})


def authors_max_price_book(request):
    authors = Author.objects.annotate(max_price=Max('books__price'))
    return render(request, 'app/max_price_book.html', {'authors': authors})


def authors_min_price_book(request):
    authors = Author.objects.annotate(min_price=Min('books__price'))
    return render(request, 'app/min_price_book.html', {'authors': authors})


def authors_min_price_average(request):
    min_prices = Author.objects.annotate(min_price=Min('books__price')).values_list('min_price', flat=True)
    avg_min_price = min_prices.aggregate(avg_min_price=Avg('min_price'))['avg_min_price']
    return render(request, 'app/min_price_average.html', {'avg_min_price': avg_min_price})

