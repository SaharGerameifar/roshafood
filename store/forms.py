from django import forms
from .models import Order
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

PRODUCT_COUNT_CHOICES = [(i, str(i)) for i in range(1, 11)]
attr = {'class': 'form-control'}


class CartAddProductForm(forms.Form):
    count = forms.TypedChoiceField(choices=PRODUCT_COUNT_CHOICES,
                                   coerce=int,
                                   initial=1,
                                   widget=forms.HiddenInput
                                   )
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)


class CartUpdateProductForm(forms.Form):
    count = forms.TypedChoiceField(choices=PRODUCT_COUNT_CHOICES,
                                   coerce=int,
                                   initial=1,
                                   )
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)

class OrderCheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('name', 'family', 'email', 'mobile', 'address')
        labels = {
            'name': 'نام',
            'family': 'نام خانوادگی',
            'email': 'ایمیل',
            'mobile': 'موبایل',
            'address': 'آدرس',
        }
        widgets = {
            'name': forms.TextInput(attrs=attr),
            'family': forms.TextInput(attrs=attr),
            'mobile': forms.TextInput(attrs=attr),
            'email': forms.EmailInput(attrs=attr),
            'address': forms.Textarea(attrs=attr),
        }


