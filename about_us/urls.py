from django.urls import path
from . import views

urlpatterns = [
    path('about-us', views.about_us_page, name='about_us_page'),
]
