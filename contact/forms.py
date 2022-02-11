from django import forms
from .models import Contact

attr = {'class': 'form-control'}


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'mobile', 'email', 'message']
        labels = {
            'name': 'نام',
            'mobile': 'موبایل',
            'email': 'ایمیل',
            'message': 'متن پیام'
        }
        widgets = {
            'name': forms.TextInput(attrs=attr),
            'mobile': forms.TextInput(attrs=attr),
            'email': forms.EmailInput(attrs=attr),
            'message': forms.Textarea(attrs=attr)
        }
      
