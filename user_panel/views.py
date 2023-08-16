from django.shortcuts import render
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView, View
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from user_account.models import User, Profile
from user_panel.forms import UserPanelOriginForm, ProfileForm, PanelChangePassword


# Create your views here.

# @method_decorator(login_required, name='dispatch')
class UserPanelAdminView(View):
    def get(self, request: HttpRequest):
        user_id = request.user.id
        user = User.objects.filter(id=user_id).first()
        profile_user = Profile.objects.filter(user_id=user_id).first()
        origin_form = UserPanelOriginForm(instance=user)
        profile_form = ProfileForm(instance=profile_user)
        password_form = PanelChangePassword()
        context = {
            'origin_form': origin_form,
            'profile_form': profile_form,
            'password_form': password_form,
            'user': user,
        }
        return render(request, 'user_panel/user_panel.html', context)

    def post(self, request: HttpRequest):
        user_id = request.user.id
        post = request.POST

        user = User.objects.filter(id=user_id).first()
        profile_user = Profile.objects.filter(user_id=user_id).first()

        if request.method == 'POST':
            if 'save_user_edit' in post:
                origin_form = UserPanelOriginForm(post, request.FILES, instance=user)
                profile_form = ProfileForm(instance=profile_user)
                password_form = PanelChangePassword()
                if origin_form.is_valid():
                    origin_form.save(commit=True)
            elif 'delete_avatar' in post:
                profile_form = ProfileForm(instance=profile_user)
                origin_form = UserPanelOriginForm(post, request.FILES, instance=user)
                password_form = PanelChangePassword()
                user.avatar.delete()
            elif 'save_profile_edit' in post:
                origin_form = UserPanelOriginForm(instance=user)
                profile_form = ProfileForm(request.POST, instance=profile_user)
                password_form = PanelChangePassword()
                if profile_form.is_valid():
                    profile_form.save(commit=True)
            elif 'change_password' in request.POST:
                origin_form = UserPanelOriginForm(instance=user)
                profile_form = ProfileForm(instance=profile_user)
                password_form = PanelChangePassword(request.POST)
                if password_form.is_valid():
                    current_password = password_form.cleaned_data['current_password']
                    password_check = user.check_password(current_password)
                    if password_check:
                        new_password = password_form.cleaned_data['password']
                        user.set_password(new_password)
                        user.save()
                        logout(request)
                        request.session['panel_change_pass'] = 'True'
                        return redirect(reverse('sign_in'))
                    else:
                        password_form.add_error('current_password', 'رمز عبور شما صحیح نمی باشد')

        context = {
            'password_form': password_form,
            'origin_form': origin_form,
            'profile_form': profile_form,
            'user': user,
        }
        return render(request, 'user_panel/user_panel.html', context)
