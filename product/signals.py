import json
import os

from django.core.mail import send_mail
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver

from config import settings
from config.settings import EMAIL_DEFAULT_SENDER
from customer.models import User
from product.models import Product


@receiver(post_save, sender=Product)
def post_save_product(sender, instance, created, **kwargs):
    if created:
        print('Product has been created')
        subject = 'New Product Added'
        message = f'Product {instance.name} has been successfully added.'
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


@receiver(pre_delete, sender=Product)
def pre_delete_product(sender, instance, **kwargs):
    filename = os.path.join(settings.BASE_DIR, 'products_data', f'{instance.slug}.json')
    product_data = {
        'id': instance.id,
        'name': instance.name,
        'price': str(instance.price),
        'description': instance.description,
        'image': str(instance.image),
        'slug': instance.slug
    }

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, mode='w') as f:
        json.dump(product_data, f, indent=4)

    print('Product data saved before deletion')
