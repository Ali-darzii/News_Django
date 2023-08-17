from django.shortcuts import render
from django.views.generic.base import TemplateView, View
from django.views.generic import ListView, DetailView

from product.models import Product


class ProductListView(ListView):
    template_name = 'products/product_list_page.html'
    model = Product
    ordering = ['-price']
    paginate_by = 9

