import json
import os
from datetime import datetime

from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver

from config import settings
from config.settings import EMAIL_DEFAULT_SENDER, BASE_DIR
from customer.models import Customer, User


def pre_save_customer(sender, instance, *args, **kwargs):
    print('Before saving')


pre_save.connect(pre_save_customer, sender=Customer)

#
# def post_save_customer(sender, instance, created, *args, **kwargs):
#     if created:
#         print('After saving')
#
#
# post_save.connect(post_save_customer, sender=Customer)


@receiver(post_save, sender=Customer)
def post_save_customer(sender, instance, created, **kwargs):
    if created:
        subject = 'Welcome to Our Platform'
        message = f'Hello {instance.full_name}, thank you for registering as a customer!'
        from_email = 'jamoliddinshodmonov89@example.com'
        recipient_list = [instance.email]
        send_mail(subject, message, from_email, recipient_list)


@receiver(pre_delete, sender=Customer)
def save_deleted_customer(sender, instance, *args, **kwargs):
    current_date = datetime.now()

    filename = os.path.join(BASE_DIR, 'customers_data', f'{instance.full_name}.json')
    customer_data = {
        'id ': instance.id,
        'full_name': instance.full_name,
        'email': instance.email,
        'phone': instance.phone,
        'address': instance.address,
        'image': str(instance.image),
        'slug': instance.slug
    }
    with open(filename, mode='w') as f:
        json.dump(customer_data, f, indent=4)

    print('Customer successfully deleted')


def pre_save_user(sender, instance, *args, **kwargs):
    print('Before saving')


@receiver(post_save, sender=User)
def post_save_user(sender, instance, created, **kwargs):
    if created:
        print('User has been created')
        subject = 'New User Created'
        message = f'User {instance.username} has been created successfully.'
        from_email = EMAIL_DEFAULT_SENDER
        recipient_list = [admin.email for admin in User.objects.filter(is_staff=True)]

        if recipient_list:
            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=recipient_list,
                fail_silently=False
            )


@receiver(pre_delete, sender=User)
def pre_delete_user(sender, instance, **kwargs):
    filename = os.path.join(settings.BASE_DIR, 'users_data', f'{instance.username}.json')
    user_data = {
        'id': instance.id,
        'username': instance.username,
        'email': instance.email,
        'first_name': instance.first_name,
        'last_name': instance.last_name
    }

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, mode='w') as f:
        json.dump(user_data, f, indent=4)

    print('User data saved before deletion')

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, mode='w') as f:
        json.dump(user_data, f, indent=4)

    print('User data saved before deletion')
