from django.http import HttpRequest
from django.shortcuts import render
from django.views.generic.base import TemplateView


class HomeView(TemplateView):
    template_name = 'home/index.html'


def site_header_components(request: HttpRequest):
    return render(request, 'shared/site_header_component.html')


def site_footer_components(request: HttpRequest):
    return render(request, 'shared/site_footer_component.html')
