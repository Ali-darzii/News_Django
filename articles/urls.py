from django.http import HttpRequest
from django.urls import path
from . import views

urlpatterns = [
    path('cat/<str:category>/', views.article_tech_list, name='article_tech_list'),
    path('load-more/', views.article_list_load_more, name='load_more_tech_article'),
    path('news/<slug:slug>/', views.ArticleDetail.as_view(), name='article_detail'),
    path('like/process/', views.article_like, name='article_like_process'),

]
