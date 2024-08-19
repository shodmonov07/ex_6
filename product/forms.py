from django import forms

from product.models import Product


class ProductForm(forms.Form):
    name = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    price = forms.FloatField()
    rating = forms.FloatField()
    discount = forms.IntegerField()
    quantity = forms.IntegerField()


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ()
