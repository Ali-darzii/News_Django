from django.core.exceptions import ValidationError
from django.http import HttpRequest, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string

from django.views.generic.base import TemplateView, View
from .forms import SignupForm, SignInFrom, ForgetPasswordForm, ResetPasswordForm
from django.urls import reverse
from django.contrib.auth import login, logout
from utils.email_service import send_email
from utils.validators import password_compair
import sweetify
from .models import User, Profile
from django.contrib.auth.password_validation import validate_password
import json


class SignUpView(View):

    def get(self, request: HttpRequest):
        # captcha: session_check and refresh_check and send data to form
        captcha_counter = request.session.get('captcha_counter_signup')
        if captcha_counter is None:
            captcha_counter = request.session['captcha_counter_signup'] = 0
        kwarg_signup = {'captcha_counter_signup': captcha_counter}
        signup_form = SignupForm(kwarg_signup=kwarg_signup)
        # In/visible captcha
        captcha_status = False
        if captcha_counter >= 2:
            captcha_status = True
        # render
        context = {
            'form': signup_form,
            'captcha_active': captcha_status
        }
        return render(request, 'user_account/signup.html', context)

    def post(self, request: HttpRequest, **kwargs):
        # captcha: get_session and send data to form
        captcha_counter = request.session.get('captcha_counter_signup')
        kwarg_signup = {'captcha_counter_signup': captcha_counter}
        signup_form = SignupForm(request.POST, kwarg_signup=kwarg_signup)
        # In/visible captcha
        captcha_status = False
        if captcha_counter >= 2:
            captcha_status = True
        request.session['captcha_counter_signup'] += 1
        if request.user.is_authenticated:
            logout(request)
        if request.method == 'POST':
            if signup_form.is_valid():

                password = signup_form.cleaned_data['password']
                email = signup_form.cleaned_data['email']
                user_exist: bool = User.objects.filter(email__iexact=email).exists()

                if user_exist:
                    signup_form.add_error('email', 'کاربری قبلا با این ایمیل ثبت نام کرده است')
                else:
                    new_user = User(email=email, email_active_code=get_random_string(72), is_active=False,
                                    username=email)
                    new_user.set_password(password)
                    new_user.save()
                    del request.session['captcha_counter_signup']
                    send_email('فعال سازی حساب کاربری ', new_user.email, {'user': new_user},
                               'emails/activate_account.html')
                    sweetify.sweetalert(request, 'عملیات موفق', icon='success',
                                        text='ایمیلی حاوی لینک تایید حساب کاریری ارسال شد.',
                                        button='<a style="color:white;" href="http://127.0.0.1:8000/sign-in">رفتن به صفحه ورود</a>',
                                        persistent=True
                                        )

        context = {
            'form': signup_form,
            'captcha_active': captcha_status
        }
        return render(request, 'user_account/signup.html', context)


class ActivateAccountView(View):
    def get(self, request: HttpRequest, email_active_code):
        user: User = User.objects.filter(email_active_code__iexact=email_active_code).first()
        if user is not None:
            if not user.is_active:
                user.is_active = True
                user.email_active_code = (get_random_string(72))
                # bane or
                # delete his account
                user.save()
                user_profile: Profile = Profile(user_id=user.id)
                user_profile.save()
                request.session['new_active'] = 'True'
                return redirect(reverse('sign_in'))
            else:
                raise Http404
        raise Http404


# we can use django-alluth for social auth
class SignInView(View):
    def get(self, request: HttpRequest):
        captcha_counter = request.session.get('captcha_counter')
        if captcha_counter is None:
            captcha_counter = request.session['captcha_counter'] = 0
        kwarg = {'captcha_active': captcha_counter}
        signin_form = SignInFrom(kwarg=kwarg)

        new_active = request.session.get('new_active')
        if new_active is not None:
            sweetify.sweetalert(request, 'عملیات موفق', icon='info',
                                text='حساب کاربری شما فعال شد و می توانید ورود کنید',
                                button='ok',
                                persistent=True
                                )
            del request.session['new_active']

        user_found = request.session.get('user_found_reset')
        # if user_found is not None:
        #     sweetify.sweetalert(request, 'عملیات موفق', icon='success',
        #                         text='رمز حساب کاربری شما تغییر یافت و می توانید ورود کنید',
        #                         button='ok',
        #                         persistent=True
        #                         )
        #     del request.session['user_found_reset']

        panel_change_pass = request.session.get('panel_change_pass')
        if panel_change_pass is not None:
            sweetify.sweetalert(request, 'عملیات موفق', icon='success',
                                text='رمز حساب کاربری شما تغییر یافت و می توانید ورود کنید',
                                button='ok',
                                persistent=True
                                )
            del request.session['panel_change_pass']


        # In/visible captcha
        captcha_status = False
        if captcha_counter >= 2:
            captcha_status = True
        context = {
            'form': signin_form,
            'captcha_active': captcha_status
        }
        return render(request, 'user_account/signin.html', context)

    def post(self, request: HttpRequest, **kwargs):
        # captcha: get_session and send data to form
        captcha_counter = request.session.get('captcha_counter')
        kwarg = {'captcha_active': captcha_counter}
        signin_form = SignInFrom(request.POST, kwarg=kwarg)

        if request.method == 'POST':
            if not request.user.is_authenticated:
                request.session['captcha_counter'] += 1
                if signin_form.is_valid():
                    email = signin_form.cleaned_data['email']
                    user: User = User.objects.filter(email__iexact=email).first()
                    if user is not None:
                        if user.is_active:
                            password = signin_form.cleaned_data['password']
                            password_check = user.check_password(password)
                            if password_check:
                                del request.session['captcha_counter']
                                remember_me = signin_form.cleaned_data.get('remember_me')
                                if not remember_me:
                                    request.session.set_expiry(0)
                                login(request, user)
                                return redirect(reverse('user_panel'))
                            else:
                                signin_form.add_error('email', 'ایمیل یا رمز عبور اشتباه وارد شده')
                        else:
                            signin_form.add_error('email', 'حساب کاربری شما فعال نشده')
                    else:
                        signin_form.add_error('email', 'ایمیل یا رمز عبور اشتباه وارد شده')
            else:
                signin_form.add_error('email', 'شما در حال حاضر در حساب کاربری دیگری هستید')
        # In/visible captcha
        captcha_status = False
        if captcha_counter >= 2:
            captcha_status = True

        context = {
            'form': signin_form,
            'captcha_active': captcha_status
        }

        return render(request, 'user_account/signin.html', context)


class ForgetPasswordView(View):
    def get(self, request: HttpRequest):
        forget_pass_counter = request.session.get('forg_counter')
        if forget_pass_counter is None:
            forget_pass_counter = request.session['forg_counter'] = 0
        kwarg_forg = {'forg_counter': forget_pass_counter}
        forget_form = ForgetPasswordForm(kwarg_forg=kwarg_forg)

        captcha_active = False
        if forget_pass_counter >= 2:
            captcha_active = True

        context = {
            'form': forget_form,
            'captcha_active': captcha_active
        }
        return render(request, 'user_account/forget_password_page.html', context)

    def post(self, request: HttpRequest):
        # send data to check captcha_required
        forget_pass_counter = request.session.get('forg_counter')
        kwarg_forg = {'forg_counter': forget_pass_counter}
        forget_form = ForgetPasswordForm(request.POST, kwarg_forg=kwarg_forg)

        # In/visible captcha
        captcha_active = False
        if forget_pass_counter >= 2:
            captcha_active = True

        if request.method == 'POST':
            request.session['forg_counter'] += 1
            if forget_form.is_valid():
                email = forget_form.cleaned_data.get('email')
                user: User = User.objects.filter(email__iexact=email).first()
                if user is not None:
                    send_email('فراموشی رمز عبور', user.email, {'user': user}, 'emails/forgotten_password.html')
                    del request.session['forg_counter']
                    sweetify.sweetalert(request, 'عملیات موفق', icon='success',
                                        text='ایمیلی حاوی لینک برای تغییر رمز خود فرستاده شد.',
                                        button='OK',
                                        persistent=True
                                        )
                else:
                    forget_form.add_error('email', 'حساب کاریری با این ایمیل یافت نشد')
        context = {
            'form': forget_form,
            'captcha_active': captcha_active
        }
        return render(request, 'user_account/forget_password_page.html', context)


class ResetPasswordView(View):
    def get(self, request: HttpRequest, active_code):
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if user is None:
            return redirect(reverse('sign_up'))
        reset_form = ResetPasswordForm()
        context = {
            'user': user,
            'form': reset_form
        }
        return render(request, 'user_account/reset_password_page.html', context)

    def post(self, request: HttpRequest, active_code):
        reset_form = ResetPasswordForm(request.POST)
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if request.method == 'POST' and reset_form.is_valid():
            if user is not None:
                password = reset_form.cleaned_data['password']
                same_password = user.check_password(password)
                if not same_password:
                    user.set_password(password)
                    user.email_active_code = get_random_string(72)
                    user.is_active = True
                    user.save()
                    request.session['user_found_reset'] = 'True'
                    return redirect(reverse('sign_in'))
                else:
                    reset_form.add_error('password', 'رمز وارد شده رمز قبلی است, لطفا رمز جدیدی وارد کنید')

            else:
                request.session['user_not_found_reset'] = 'True'
                return redirect(reverse('contact_us_page'))
        context = {
            'form': reset_form,
            'user': user
        }
        return render(request, 'user_account/reset_password_page.html', context)


class SignOut(View):
    def get(self, request: HttpRequest):
        logout(request)
        return redirect(reverse('index_page'))
