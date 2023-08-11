from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField
from captcha import fields
from django.http import HttpRequest


class SignupForm(forms.Form):
    def __init__(self, *args, **kwargs):
        captcha_pop = kwargs.pop('kwarg_signup', None)
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['email'] = forms.CharField(
            label='پست الکترونیکی',
            validators=[
                validators.EmailValidator(message='ایمیل معتبر وارد کنید'),
            ],
            required=True,
            widget=forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'id': 'emailsignup',
                'placeholder': 'ایمیل',
                'aria-describedby': 'emailHelp'
            }))

        self.fields['password'] = forms.CharField(
            label='رمز عبور',
            widget=forms.PasswordInput(attrs={
                'class': 'form-control',
                'id': 'passworddignup',
                'placeholder': '*********',

            }))

        self.fields['confirm_password'] = forms.CharField(
            label='تایید رمز عبور',
            # required=True,
            widget=forms.PasswordInput(attrs={
                'class': 'form-control',
                'id': 'confirmpassworddignup',
                'placeholder': '*********',
            }))
        # captcha required status
        captcha_counter = captcha_pop.get('captcha_active_signup')
        captcha_status: bool = False
        if captcha_counter >= 2:
            captcha_status: bool = True

        self.fields['captcha'] = captcha = CaptchaField(label='(لطفا متن داخل تصویر را وارد کنید)',
                                                        required=captcha_status)

    def clean(self):
        clean = super().clean()
        password = clean.get('password')
        confirm_password = clean.get('confirm_password')
        # Pair Password
        if password != confirm_password:
            self.add_error('password', 'رمز شما مطابقت ندارد')
        # password > 6
        elif not 6 < len(password) < 30:
            self.add_error('password', 'رمز شما باید بین 6 تا 30 حرف باشد')

        return clean


class SignInFrom(forms.Form):
    def __init__(self, *args, **kwargs):
        captcha_pop = kwargs.pop('kwarg', None)
        super(SignInFrom, self).__init__(*args, **kwargs)
        self.fields['email'] = forms.CharField(
            label='پست الکترونیکی',
            required=True,
            widget=forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'id': 'emailsignup',
                'placeholder': 'ایمیل',
                'aria-describedby': 'emailHelp'
            }),
            validators=[
                validators.EmailValidator
            ]
        )
        self.fields['password'] = forms.CharField(
            label='رمز عبور',
            required=True,
            widget=forms.PasswordInput(attrs={
                'class': 'form-control',
                'id': 'passworddignup',
                'placeholder': '*********',

            }),
        )
        # captcha required status
        captcha_counter = captcha_pop.get('captcha_active')
        captcha_status: bool = False
        if captcha_counter >= 2:
            captcha_status: bool = True
        self.fields['captcha'] = CaptchaField(label='(لطفا متن داخل تصویر را وارد کنید)', required=captcha_status)

        self.fields['remember_me'] = forms.BooleanField(label='مرا به خاطر بسپار', required=False, initial=True,
                                                        widget=forms.CheckboxInput(attrs={
                                                            'class': 'form-check-input',
                                                            'id': 'remember-me',
                                                        }))


class ForgetPasswordForm(forms.Form):
    def __init__(self, *args, **kwargs):
        captcha_pop = kwargs.pop('kwarg_forg', None)
        super(ForgetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['email'] = forms.CharField(
            label='پست الکترونیکی',
            required=True,
            widget=forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'id': 'emailsignup',
                'placeholder': 'ایمیل',
                'aria-describedby': 'emailHelp'
            }),
            validators=[
                validators.EmailValidator
            ]
        )

        captcha_counter = captcha_pop.get('forg_counter')
        captcha_status: bool = False
        if captcha_counter >= 2:
            captcha_status: bool = True
        self.fields['captcha'] = CaptchaField(label='(لطفا متن داخل تصویر را وارد کنید)', required=captcha_status)
