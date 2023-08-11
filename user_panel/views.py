from django.shortcuts import render
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView, View
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


# Create your views here.

# @method_decorator(login_required, name='dispatch')
class UserPanelAdminView(View):
    def get(self, request: HttpRequest):
        return render(request, 'user_panel/user_panel.html')

    def post(self, request: HttpRequest):
        pass
