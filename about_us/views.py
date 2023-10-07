from django.http import HttpResponse
from django.shortcuts import render

from about_us.models import AboutUs, Expert


# Create your views here.
def about_us_page(request: HttpResponse):
    about_us = AboutUs.objects.filter(is_active=True).first()
    experts = Expert.objects.filter(is_active=True).all()
    context = {
        'about_us': about_us,
        'experts': experts
    }
    return render(request, 'about_us/about_us_template.html', context)
