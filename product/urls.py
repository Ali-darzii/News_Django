from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list, name='product_list_page'),
    path('products/filterProduct/', views.filterProduct, name='filterProduct'),
    path('products/search/', views.search, name='search_filter'),
    path('products/<slug:slug>', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/comment/', views.product_comment, name='product_comment'),
    path('products/comment/like-dislike/', views.like_dislike, name='like_dislike'),
]
