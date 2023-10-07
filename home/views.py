from django.http import HttpRequest
from django.shortcuts import render
from django.views.generic.base import TemplateView
import sweetify

from articles.models import Article, ArticleCategory
from home.models import Slider
from order_basket.models import OrderDetail, Order
from user_account.models import User


def HomeView(request: HttpRequest):
    deleted_account = request.session.get('deleted_account')
    if deleted_account is not None:
        sweetify.sweetalert(request, 'عملیات موفق', icon='info',
                            text='حساب کاربری شما حذف شد!',
                            button='OK',
                            persistent=True
                            )
        del request.session['deleted_account']
    slider: Slider = Slider.objects.filter(is_active=True).all()
    article: Article = Article.objects.filter(is_active=True).order_by('-create_date')[:9]
    context = {
        'sliders': slider,
        'articles': article
    }

    return render(request, 'home/index.html', context)


def site_header_components(request: HttpRequest):
    user = User.objects.filter(id=request.user.id).first()
    article_categories = ArticleCategory.objects.filter(is_active=True)
    if request.user.is_authenticated:
        current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                                 user_id=request.user.id)
        total_amount = current_order.calculate_total_price()
        product_in_basket = current_order.count_total_products()
        context = {
            'user': user,
            'product_count': product_in_basket,
            'order': current_order,
            'sum': total_amount,
            'article_categories': article_categories
        }
    else:
        context = {
            'user': user,
            'count_is_zero': True,
            'article_categories': article_categories

        }
    return render(request, 'shared/site_header_component.html', context)


def site_footer_components(request: HttpRequest):
    return render(request, 'shared/site_footer_component.html')
