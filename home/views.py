from django.http import HttpRequest
from django.shortcuts import render
from django.views.generic.base import TemplateView
import sweetify

from user_account.models import User


class HomeView(TemplateView):
    template_name = 'home/index.html'

    def setup(self, request, *args, **kwargs):
        setup = super().setup(request)
        deleted_account = request.session.get('deleted_account')
        if deleted_account is not None:
            sweetify.sweetalert(request, 'عملیات موفق', icon='info',
                                text='حساب کاربری شما حذف شد!',
                                button='OK',
                                persistent=True
                                )
            del request.session['deleted_account']


def site_header_components(request: HttpRequest):
    user = User.objects.filter(id=request.user.id).first()
    return render(request, 'shared/site_header_component.html', context={'user': user})


def site_footer_components(request: HttpRequest):
    return render(request, 'shared/site_footer_component.html')
