from decimal import Decimal

from django.db import models


class Product(models.Model):
    class RatingChoices(models.IntegerChoices):
        zero = 0
        one = 1
        two = 2
        three = 3
        four = 4
        five = 5

    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    image = models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    rating = models.PositiveSmallIntegerField(choices=RatingChoices.choices, default=RatingChoices.zero.value,
                                              null=True, blank=True)
    discount = models.PositiveSmallIntegerField(null=True, blank=True)
    quantity = models.IntegerField(default=0)

    def get_attributes(self) -> list[dict]:
        product_attributes = ProductAttribute.objects.filter(product=self)
        attributes = []
        for pa in product_attributes:
            attributes.append({
                'attribute_key': pa.attribute.key_name,
                'attribute_value': pa.attribute_value.value_name
            })
        return attributes

    @property
    def discounted_price(self):
        if self.discount > 0:
            discount_decimal = Decimal(self.discount) / Decimal(100)
            return self.price * (1 - discount_decimal)
        return self.price

    def __str__(self):
        return self.name

# python manage.py makemigrations


class Attribute(models.Model):
    key_name = models.CharField(max_length=125, unique=True)

    def __str__(self):
        return self.key_name


class AttributeValue(models.Model):
    value_name = models.CharField(max_length=125, unique=True)

    def __str__(self):
        return self.value_name


class ProductAttribute(models.Model):
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    attribute = models.ForeignKey('product.Attribute', on_delete=models.CASCADE)
    attribute_value = models.ForeignKey('product.AttributeValue', on_delete=models.CASCADE)
