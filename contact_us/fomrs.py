from django import forms
from django.core import validators

from django.core.exceptions import ValidationError


class ContactUsForm(forms.Form):
    full_name = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'fname_contact-us',
        'placeholder': 'نام و نام خانوادگی'
    }))
    email = forms.CharField(
                            validators=[validators.EmailValidator(message='ایمیل معتبر وارد کنید')],
                            required=True, label='ایمیل',
                            widget=forms.TextInput(attrs={
                                'class': 'form-control',
                                'id': 'email_contact-us',
                                'placeholder': 'ایمیل'
                            }),

                            )
    title = forms.CharField(max_length=30, required=True, widget=forms.TextInput({
        'class': 'form-control',
        'id': 'title_contact-us',
        'placeholder': 'عنوان'

    }))
    text_massege = forms.CharField(max_length=200, required=True, widget=forms.Textarea(attrs={
        'class': 'form-control self-text-area',
        'id': 'textmassage_contact-us',
        'placeholder': 'متن درخواست',
        'rows': '6',
        'cols': '40',
    }))

