from django.urls import path

from app import views

urlpatterns = [
    path('book-count/', views.authors_book_count, name='authors_book_count'),
    path('max-price-book/', views.authors_max_price_book, name='authors_max_price_book'),
    path('min-price-book/', views.authors_min_price_book, name='authors_min_price_book'),
    path('min-price-average/', views.authors_min_price_average, name='authors_min_price_average'),
]