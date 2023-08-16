from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import re

from user_account.models import User, Profile


class UserPanelOriginForm(forms.ModelForm):
    disabled = True
    email = forms.CharField(max_length=100, required=True, disabled=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'example@gmail.com',
        'disable': 'True'
    }), )

    class Meta:
        model = User

        fields = {'first_name', 'last_name', 'avatar', 'email', 'city', 'about_user', 'birth'}

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام خانوادگی'
            }),
            'avatar': forms.FileInput(attrs={
                'type': "file",
                'class': 'imageInput',
                'id': 'imageInput',
                'accept': 'image/*"'

            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'تهران'
            }),
            'about_user': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '3',
                'cols': '4'

            }),
            'birth': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'DD/MM/YYYY'

            })
        }

    def clean(self):
        clean = super().clean()
        first_name = clean.get('first_name')
        last_name = clean.get('last_name')
        city = clean.get('city')

        # in first and last name use persian and don't use numbers
        if re.findall('[A-Z]', first_name) or re.findall('[a-z]', first_name):
            self.add_error('first_name', 'لطفا از زبان فارسی استفاده کنید')
        elif re.findall('[0-9]', first_name):
            self.add_error('first_name', 'لطفا از عدد استفاده نکنید!')

        elif re.findall('[A-Z]', last_name) or re.findall('[a-z]', last_name):
            self.add_error('last_name', 'لطفا از زبان فارسی استفاده کنید')
        elif re.findall('[0-9]', last_name):
            self.add_error('last_name', 'لطفا از عدد استفاده نکنید!')
        elif city is not None:
            if re.findall('[A-Z]', city) or re.findall('[a-z]', city):
                self.add_error('city', 'لطفا از زبان فارسی استفاده کنید')
            elif re.findall('[0-9]', city):
                self.add_error('city', 'لطفا از عدد استفاده نکنید!')

        return clean


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address', 'home_phone', 'post_cart']

        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '09121234567'
            }),
            'home_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '021-771234566'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '2',
                'cols': '2'
            }),
            'post_cart': forms.TextInput(attrs={
                'class': 'form-control',
            })

        }

    def clean(self):
        clean = super().clean()
        phone = clean.get('phone')
        home_phone = clean.get('home_phone')
        post_cart = clean.get('post_cart')
        if phone is not None:
            if not re.findall('[0-9]', phone):
                self.add_error('phone', 'لطفا فقط از ارقام استفاده کنید')
            elif not phone.startswith('09'):
                self.add_error('phone', 'شماره وارد شده درست نمی باشد')
            elif not len(phone) == 11:
                self.add_error('phone', 'شماره وارد شده درست نمی باشد')

        if home_phone is not None:
            if not re.findall('[0-9]', home_phone):
                self.add_error('home_phone', 'لطفا فقط از ارقام استفاده کنید')
            elif not home_phone.startswith('0'):
                self.add_error('home_phone', 'لطفا پیش شماره شهر خود را وارد کنید')
            elif not len(home_phone) == 11:
                self.add_error('home_phone', 'شماره وارد شده درست نمی باشد')

        if post_cart is not None:
            if len(post_cart) < 10:
                self.add_error('post_cart', 'شماره وارد شده درست نمی باشد')
        return clean


class PanelChangePassword(forms.Form):
    current_password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'currentpassword',
            'placeholder': '*********',

        }))

    password = forms.CharField(
        label='رمز عبور جدید',
        # required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'pass_show',
            'name': 'pass-show',
            'placeholder': '*********',
        }))
    confirm_password = forms.CharField(
        label='تایید رمز عبور',
        # required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'confirmpassword',
            'placeholder': '*********',
        }))

    def clean(self):
        clean = super().clean()
        password = clean.get('password')
        confirm_password = clean.get('confirm_password')
        if not re.findall('[a-z]', password) or not re.findall('[a-z]', password):
            self.add_error('password', 'لطفا از زبان انگیلیسی استفاده کنید')
        # Pair Password
        elif not password == confirm_password:
            self.add_error('password', 'رمز شما مطابقت ندارد')
        # password > 6
        elif not 6 < len(password) < 30:
            self.add_error('password', 'رمز شما باید بین 7 تا 30 عدد یا حرف باشد')

        return clean


class DeleteAccountForm(forms.Form):
    delete_check = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input',
        'id': 'deleteaccountCheck',
    }))
