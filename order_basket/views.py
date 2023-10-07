from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from articles.models import ArticleCategory
from order_basket.models import Order, OrderDetail
from product.models import Product
from django.contrib.auth.decorators import login_required


def add_product_to_order(request: HttpRequest):
    product_id = request.GET.get('product_id')
    count = int(request.GET.get('count'))
    if count < 1:
        return JsonResponse({
            'status': 'invalid_count'
        })
    elif request.user.is_authenticated:
        product: Product = Product.objects.filter(pk=product_id, is_active=True, is_delete=False).first()
        if product is not None:
            current_order, created = Order.objects.get_or_create(user_id=request.user.id, is_paid=False)
            current_detail_order = current_order.orderdetail_set.filter(product_id=product_id).first()
            if current_detail_order is not None:
                current_detail_order.count += count
                current_detail_order.save()
                current_orders, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                                          user_id=request.user.id)
                products_in_basket_count = current_orders.count_total_products()
                total_amount = current_orders.calculate_total_price()
                return JsonResponse({
                    'status': 'success',
                    'orderCount': render_to_string('ajax/ajax_order_count_header.html',
                                                   context={'product_count': products_in_basket_count}),
                    'orderBasket': render_to_string('ajax/header_basket_order.html', context={
                        'order': current_orders,
                        'sum': total_amount
                    })
                })
            else:
                new_detail = OrderDetail(product_id=product_id, order_id=current_order.id, count=count)
                new_detail.save()
                current_orders, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                                          user_id=request.user.id)
                products_in_basket_count = current_orders.count_total_products()
                total_amount = current_orders.calculate_total_price()
                return JsonResponse({
                    'status': 'success',
                    'orderCount': render_to_string('ajax/ajax_order_count_header.html',
                                                   context={'product_count': products_in_basket_count}),
                    'orderBasket': render_to_string('ajax/header_basket_order.html', context={
                        'order': current_orders,
                        'sum': total_amount
                    })
                })
        else:
            return JsonResponse({
                'status': 'product_not_found'
            })
    else:
        return JsonResponse({
            'status': 'not_auth'
        })


@login_required
def change_order_detail_count(request: HttpRequest):
    detail_id = request.GET.get('detail_id')
    state = request.GET.get('state')

    if detail_id is None or state is None:
        return JsonResponse({
            'status': 'not_found_detail_or_status'
        })
    order_detail = OrderDetail.objects.filter(pk=detail_id, order__user_id=request.user.id,
                                              order__is_paid=False).first()

    if order_detail is None:
        return JsonResponse({
            'status': 'Detail_not_found'
        })

    if state == 'increase':
        order_detail.count += 1
        order_detail.save()

    elif state == 'decrease':
        if order_detail.count == 1:
            order_detail.delete()
        else:
            order_detail.count -= 1
            order_detail.save()
    else:
        return JsonResponse({
            'status': 'state_invalid'
        })
    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                             user_id=request.user.id)
    total_amount = current_order.calculate_total_price()
    products_in_basket_count = current_order.count_total_products()
    return JsonResponse({
        'status': 'success',
        'orderCount': render_to_string('ajax/ajax_order_count_header.html', context={
            'product_count': products_in_basket_count
        }),
        'orderBasket': render_to_string('ajax/header_basket_order.html', context={
            'order': current_order,
            'sum': total_amount
        })

    })


@login_required
def remove_order_detail(request: HttpRequest):
    detail_id = int(request.GET.get('detail_id'))
    if detail_id is None:
        return JsonResponse({
            'status': 'not_found_detail_id'
        })

    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                             user_id=request.user.id)
    detail = current_order.orderdetail_set.filter(pk=detail_id, order__is_paid=False,
                                                  order__user_id=request.user.id).first()

    if detail is None:
        return JsonResponse({
            'status': 'detail_not_found'
        })
    else:
        detail.delete()

    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                             user_id=request.user.id)

    total_amount = current_order.calculate_total_price()
    products_in_basket_count = current_order.count_total_products()
    return JsonResponse({
        'status': 'success',
        'orderCount': render_to_string('ajax/ajax_order_count_header.html', context={
            'product_count': products_in_basket_count
        }),
        'orderBasket': render_to_string('ajax/header_basket_order.html', context={
            'order': current_order,
            'sum': total_amount
        })

    })


@login_required
def order_basket_view(request: HttpRequest):
    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                             user_id=request.user.id)
    total_amount = current_order.calculate_total_price()
    products_in_basket_count = current_order.count_total_products()
    tax = int((total_amount * 9) / 100)
    final_total_amount = int(total_amount + tax) + 10000
    article_categories = ArticleCategory.objects.filter(is_active=True)
    context = {
        'product_count': products_in_basket_count,
        'order': current_order,
        'sum': total_amount,
        'tax': tax,
        'final_price': final_total_amount,
        'article_categories': article_categories,

    }
    return render(request, 'order_basket/order_basket_page.html', context)


@login_required
def change_order_detail_count_in_basket_page(request: HttpRequest):
    detail_id = request.GET.get('detail_id')
    state = request.GET.get('state')

    if detail_id is None or state is None:
        return JsonResponse({
            'status': 'not_found_detail_or_status'
        })
    order_detail = OrderDetail.objects.filter(pk=detail_id, order__user_id=request.user.id,
                                              order__is_paid=False).first()

    if order_detail is None:
        return JsonResponse({
            'status': 'Detail_not_found'
        })

    if state == 'increase':
        order_detail.count += 1
        order_detail.save()

    elif state == 'decrease':
        if order_detail.count == 1:
            order_detail.delete()
        else:
            order_detail.count -= 1
            order_detail.save()
    else:
        return JsonResponse({
            'status': 'state_invalid'
        })
    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                             user_id=request.user.id)
    total_amount = current_order.calculate_total_price()
    products_in_basket_count = current_order.count_total_products()
    tax = int((total_amount * 9) / 100)
    final_total_amount = int(total_amount + tax) + 10000
    return JsonResponse({
        'status': 'success',
        'data': render_to_string('ajax/ajax_order_basket_page.html', context={
            'product_count': products_in_basket_count,
            'order': current_order,
            'sum': total_amount,
            'tax': tax,
            'final_price': final_total_amount,
        })

    })


@login_required
def remove_order_detail_in_basket_page(request: HttpRequest):
    detail_id = int(request.GET.get('detail_id'))
    if detail_id is None:
        return JsonResponse({
            'status': 'not_found_detail_id'
        })

    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                             user_id=request.user.id)
    detail = current_order.orderdetail_set.filter(pk=detail_id, order__is_paid=False,
                                                  order__user_id=request.user.id).first()

    if detail is None:
        return JsonResponse({
            'status': 'detail_not_found'
        })
    else:
        detail.delete()

    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                             user_id=request.user.id)

    total_amount = current_order.calculate_total_price()
    products_in_basket_count = current_order.count_total_products()
    tax = int((total_amount * 9) / 100)
    final_total_amount = int(total_amount + tax) + 10000
    return JsonResponse({
        'status': 'success',
        'data': render_to_string('ajax/ajax_order_basket_page.html', context={
            'product_count': products_in_basket_count,
            'order': current_order,
            'sum': total_amount,
            'tax': tax,
            'final_price': final_total_amount,
        })

    })
