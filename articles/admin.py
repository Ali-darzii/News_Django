from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Article)
admin.site.register(models.ArticleGallery)
admin.site.register(models.ArticleLike)
