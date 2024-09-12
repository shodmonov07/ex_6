import json
import os

from django.core.mail import send_mail
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver

from app.models import Book
from config import settings
from config.settings import EMAIL_DEFAULT_SENDER
from customer.models import User


@receiver(post_save, sender=Book)
def post_save_book(sender, instance, created, **kwargs):
    if created:
        print('Book has been added')
        subject = 'New Book Added'
        message = f'Book {instance.title} by {instance.author} has been successfully added.'
        from_email = EMAIL_DEFAULT_SENDER
        recipient_list = [user.email for user in User.objects.all()]

        if recipient_list:
            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=recipient_list,
                fail_silently=False
            )


@receiver(pre_delete, sender=Book)
def pre_delete_book(sender, instance, **kwargs):
    filename = os.path.join(settings.BASE_DIR, 'books_data', f'{instance.name}.json')
    book_data = {
        'id': instance.id,
        'title': instance.title,
        'author': instance.author,
        'publication_date': instance.publication_date.strftime('%Y-%m-%d'),
        'slug': instance.slug
    }

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, mode='w') as f:
        json.dump(book_data, f, indent=4)

    print('Book data saved before deletion')