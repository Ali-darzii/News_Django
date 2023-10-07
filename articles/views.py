from django.http import HttpRequest, JsonResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import DetailView
from django.urls import reverse
from articles.models import Article, ArticleCategory, ArticleGallery, ArticleLike, ArticleVisit
from user_account.models import User
from utils.http_service import get_client_ip


def article_tech_list(request: HttpRequest, **kwargs):
    article_check: ArticleCategory = ArticleCategory.objects.filter(url_title__iexact=kwargs.get("category")).exists()
    if not article_check:
        raise Http404

    article_lists: Article = Article.objects.filter(is_active=True,
                                                    category__url_title__iexact=kwargs.get("category")).order_by(
        '-create_date')[:1]
    total_articles: Article = Article.objects.filter(is_active=True,
                                                     category__url_title__iexact=kwargs.get("category")).count()

    context = {
        'article_lists': article_lists,
        'total_articles': total_articles,
        'category': kwargs.get("category"),
        'head': ArticleCategory.objects.filter(url_title__iexact=kwargs.get("category")).first()
    }
    return render(request, 'articles/tech_list_template_page.html', context)


def article_list_load_more(request: HttpRequest):
    total_item = int(request.GET.get('lengths'))
    cat = request.GET.get('category')
    article_check = ArticleCategory.objects.filter(url_title__iexact=cat).exists()
    if not article_check:
        raise Http404
    limit = 1  # how many articles come
    article_lists: Article = Article.objects.filter(is_active=True, category__url_title__iexact=cat).order_by(
        '-create_date')[total_item:total_item + limit]
    if article_lists.count() <= 0:
        return JsonResponse({
            'status': 'no_articles'
        })
    return JsonResponse({
        'status': 'success',
        'data': render_to_string('articles_ajax/ajax_tech_load_more.html', context={'article_lists': article_lists})
    })


class ArticleDetail(DetailView):
    template_name = 'articles/article_detail_template.html'
    model = Article
    context_object_name = 'article'

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(is_active=True)
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['article_gallery'] = ArticleGallery.objects.filter(article_id=self.object.id).first()
        # like stuff
        article_like_check = ArticleLike.objects.filter(article_id=self.object.id).exists()
        if not article_like_check:
            ArticleLike.objects.create(article_id=self.object.id)

        context['article_like'] = ArticleLike.objects.filter(article_id=self.object.id).first()
        context['user'] = self.request.user

        # Article visit
        user = User.objects.filter(id=self.request.user.id).first()
        user_ip = get_client_ip(self.request)
        user_id = None
        if self.request.user.is_authenticated:
            user_id = self.request.user.id
        has_been_visited = ArticleVisit.objects.filter(ip__iexact=user_ip, article_id=self.object.id).exists()
        if not has_been_visited:
            new_visit = ArticleVisit(ip=user_ip, user_id=user_id, article_id=self.object.id)
            new_visit.save()
        context['visit_count'] = ArticleVisit.objects.filter(article_id=self.object.id).count()
        context['last_articles'] = Article.objects.all().order_by('-create_date')[:6]
        return context


def article_like(request: HttpRequest):
    article_id = int(request.GET.get('article_id'))
    if not request.user.is_authenticated:
        return reverse('sign_up')
    article: Article = Article.objects.filter(pk=article_id, is_active=True).first()
    if request.user in article.article_likes.users.all():
        article.article_likes.users.remove(request.user)
        return JsonResponse({
            'status': 'dis_like',
            'data': article.get_total_likes()
        })
    else:
        article.article_likes.users.add(request.user)
        return JsonResponse({
            'status': 'like',
            'data': article.get_total_likes()
        })
