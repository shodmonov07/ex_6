# Generated by Django 5.0.7 on 2024-09-10 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0008_alter_customer_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='image',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='customer/'),
        ),
    ]
