import requests
from django.db.models import Avg
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView
from product.models import Product, ProductCategory, ProductBrand, ProductGallery, ProductVisit, ProductComment, Like, \
    DisLike
from django.core.paginator import Paginator
from user_account.models import User
from utils.convertors import group_list
from utils.http_service import get_client_ip
from django.urls import reverse
from django.db.models import Q


def product_list(request: HttpRequest):
    total_product = Product.objects.count()
    products_lists: Product = Product.objects.filter(is_active=True, is_delete=False).order_by('-id').distinct()
    p = Paginator(products_lists, 2)
    page = request.GET.get('page')
    products = p.get_page(page)
    page_range = p.page_range

    context = {
        'products_page': products,
        'page_range': page_range,
        'total_product': total_product,
    }
    return render(request, "products/product_list_page.html", context)


def filterProduct(request: HttpRequest):
    categories = (request.GET.getlist('category[]'))
    brands = request.GET.getlist('brand[]')
    stars = request.GET.getlist('stars[]')
    availability = request.GET.getlist('availability[]')
    availability_check = availability[0]
    sort = request.GET.get('sort')
    if sort == 'down':
        sort = 'price'
    elif sort == 'high':
        sort = '-price'
    else:
        sort = 'title'
    if availability_check == 'available':
        products_lists = Product.objects.filter(is_active=True, is_delete=False, inventory=True).order_by(
            sort).distinct()
    else:
        products_lists = Product.objects.filter(is_active=True, is_delete=False).order_by(sort).distinct()

    if len(brands) > 0:
        products_lists = products_lists.filter(brand__id__in=brands).distinct()
    if len(categories) > 0:
        products_lists = products_lists.filter(category__id__in=categories).distinct()
    if len(stars) > 0:
        star = stars[0]
        if int(star) <= 3:
            products_lists = products_lists.filter(productcomment__star__lt=star).distinct()
        else:
            products_lists = products_lists.filter(
                Q(productcomment__star__isnull=True) | Q(productcomment__star__lte=star)).distinct()

    p = Paginator(products_lists, 2)
    page = request.GET.get('page')
    products = p.get_page(page)
    page_range = p.page_range

    if products_lists.count() == 0:
        context = {
            'product_not_found': True
        }
    else:
        context = {
            'products_page': products,
            'page_range': page_range,
        }

    t = render_to_string('ajax/product_item.html', context)

    return JsonResponse({
        'status': 'success',
        'data': t
    })


def search(request: HttpRequest):
    q = request.GET.get('q')
    sort = request.GET.get('sort')
    if q == '':
        return JsonResponse({
            'status': 'empty',
        })
    if sort == 'down':
        sort = 'price'
    elif sort == 'high':
        sort = '-price'
    else:
        sort = 'title'

    products_lists = Product.objects.filter(is_active=True, is_delete=False, title__icontains=q).order_by(sort)

    if not products_lists.exists():
        return JsonResponse({
            "status": "not_found",
        })

    p = Paginator(products_lists, 2)
    page = request.GET.get('page')
    products = p.get_page(page)
    page_range = p.page_range

    context = {
        'products_page': products,
        'page_range': page_range,
    }
    return JsonResponse({
        "status": "success",
        "data": render_to_string('ajax/product_item.html', context)
    })


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail_page.html'

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(is_active=True)
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        # product gallery in product detail
        product_gallery = ProductGallery.objects.filter(product_id=self.object.id).all()
        context['product_gallery_group'] = product_gallery

        # visit analyze
        user = User.objects.filter(id=self.request.user.id).first()
        user_ip = get_client_ip(self.request)
        user_id = None
        if self.request.user.is_authenticated:
            user_id = self.request.user.id
        has_been_visited = ProductVisit.objects.filter(ip__iexact=user_ip, product_id=self.object.id).exists()
        if not has_been_visited:
            new_visit = ProductVisit(ip=user_ip, user_id=user_id, product_id=self.object.id)
            new_visit.save()

        # product comment
        product: Product = kwargs.get('object')
        context['comments'] = ProductComment.objects.filter(product_id=product.id)
        # how many comment we have
        comments_count = ProductComment.objects.filter(product_id=product.id).count()
        context['comments_count'] = comments_count
        # Average star comments
        if comments_count == 0:
            comments_avg = 0
        else:
            comments_avg = round(
                ProductComment.objects.filter(product_id=product.id).aggregate(Avg('star'))['star__avg'],
                1)

        context['comments_avg'] = comments_avg
        # how many complete star we have
        context['comments_int'] = range(int(comments_avg))
        # how many half star we have
        half_star = False
        if int(comments_avg * 10) % 10 != 0:
            half_star = True
        context['half_star'] = half_star
        if comments_count == 0:
            context['star_5'] = 0
            context['star_4'] = 0
            context['star_3'] = 0
            context['star_2'] = 0
            context['star_1'] = 0
        else:
            x = 100 / comments_count
            context['star_5'] = int(ProductComment.objects.filter(product_id=product.id, star=5).count() * x)
            context['star_4'] = int(ProductComment.objects.filter(product_id=product.id, star=4).count() * x)
            context['star_3'] = int(ProductComment.objects.filter(product_id=product.id, star=3).count() * x)
            context['star_2'] = int(ProductComment.objects.filter(product_id=product.id, star=2).count() * x)
            context['star_1'] = int(ProductComment.objects.filter(product_id=product.id, star=1).count() * x)

        context['user'] = self.request.user
        related_products: Product = Product.objects.filter(brand_id=product.brand.id, is_delete=False,
                                                           is_active=True).exclude(pk=product.id)[:7]
        context['related_products'] = related_products

        return context


def product_comment(request: HttpRequest, **kwargs):
    text = request.GET.get('text')
    star = int(request.GET.get('star'))
    product_id = request.GET.get('Products_id')
    if len(text) < 13:
        return JsonResponse({
            'status': 'low_char'
        })
    if 5 < star < 0:
        star = 5

    comment_created = ProductComment.objects.create(product_id=product_id, user_id=request.user.id, comment=text,
                                                    star=star)
    Like.objects.create(comment_id=comment_created.id)
    DisLike.objects.create(comment_id=comment_created.id)

    comment = ProductComment.objects.filter(product_id=product_id)
    comments_avg = round(ProductComment.objects.filter(product_id=product_id).aggregate(Avg('star'))['star__avg'], 1)
    half_star = False
    if int(comments_avg * 10) % 10 != 0:
        half_star = True
    comments_count = ProductComment.objects.filter(product_id=product_id).count()
    x = 100 / comments_count

    context = {
        'comments': comment,
        'comments_count': comments_count,
        'comments_avg': comments_avg,
        'comments_int': range(int(comments_avg)),
        'half_star': half_star,
        'star_5': int(ProductComment.objects.filter(product_id=product_id, star=5).count() * x),
        'star_4': int(ProductComment.objects.filter(product_id=product_id, star=4).count() * x),
        'star_3': int(ProductComment.objects.filter(product_id=product_id, star=3).count() * x),
        'star_2': int(ProductComment.objects.filter(product_id=product_id, star=2).count() * x),
        'star_1': int(ProductComment.objects.filter(product_id=product_id, star=1).count() * x),
        'user': request.user
    }
    return JsonResponse({
        'status': 'success',
        'data': render_to_string('ajax/product_comment.html', context)
    })


def like_dislike(request: HttpRequest):
    if not request.user.is_authenticated:
        return reverse('sign_up')
    deside = request.GET.get('deside')
    comment_id = request.GET.get('comment_id')
    product_id = request.GET.get('product_id')

    comments = ProductComment.objects.filter(product_id=product_id)
    comment = get_object_or_404(ProductComment, id=comment_id)
    if deside == 'like':
        if request.user in comment.likes.users.all():
            comment.likes.users.remove(request.user)
        else:
            comment.likes.users.add(request.user)
            comment.dis_likes.users.remove(request.user)
    else:
        if request.user in comment.dis_likes.users.all():
            comment.dis_likes.users.remove(request.user)
        else:
            comment.dis_likes.users.add(request.user)
            comment.likes.users.remove(request.user)

    context = {
        'comments': comments,
        'user': request.user

    }

    return JsonResponse({
        'data': render_to_string('ajax/ajax_like_dislike.html', context)
    })


def product_category_component(request: HttpRequest):
    for_product_category = ProductCategory.objects.filter(is_active=True, is_delete=False)[:5]
    exclude = [1, 2, 3, 4, 5]
    rest_product_category = ProductCategory.objects.filter(is_active=True, is_delete=False).exclude(id__in=exclude)
    context = {
        'for_product_categories': for_product_category,
        'rest_product_categories': rest_product_category
    }
    return render(request, 'includes/product_categories_component.html', context)


def product_brand_component(request: HttpRequest):
    for_product_brand = ProductBrand.objects.filter(is_active=True)[:4]
    exclude = [1, 2, 3, 4]
    rest_product_brand = ProductBrand.objects.filter(is_active=True).exclude(id__in=exclude)
    context = {
        'for_product_brands': for_product_brand,
        'rest_product_brands': rest_product_brand

    }
    return render(request, 'includes/product_brand_component.html', context)
