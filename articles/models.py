from django.db import models
from django.urls import reverse
from jalali_date import date2jalali
from django.contrib.auth import get_user_model
from user_account.models import User


class ArticleCategory(models.Model):
    title = models.CharField(max_length=300, verbose_name='نام دسته', db_index=True)
    url_title = models.CharField(max_length=200, unique=True, verbose_name='نام در url', db_index=True)
    is_active = models.BooleanField(verbose_name='فعال/غیر فعال')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'گروه دسته بندی'


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان مقاله')
    time_to_read = models.IntegerField(default=5, verbose_name='ظول زمان خواندن مقاله')
    slug = models.SlugField(max_length=400, db_index=True, allow_unicode=True, verbose_name='عنوان در url')
    image = models.ImageField(upload_to='images/articles', verbose_name='تصویر مقاله')
    short_description = models.TextField(verbose_name='توضیحات کوتاه')
    first_paragraph = models.TextField(verbose_name='اولبن متن مقاله', null=True, blank=True)
    second_paragraph = models.TextField(verbose_name='دومین متن مقاله', null=True, blank=True)
    third_paragraph = models.TextField(verbose_name='سومین متن مقاله', null=True, blank=True)
    forth_paragraph = models.TextField(verbose_name='چهارمین متن مقاله', null=True, blank=True)
    fifth_paragraph = models.TextField(verbose_name='پنجمین متن مقاله', null=True, blank=True)
    title_text = models.CharField(verbose_name='عنوان در جملات', max_length=100, null=True, blank=True)
    first_text_after_title = models.TextField(verbose_name='اولین متن مقاله بعد عنوان', null=True, blank=True)
    second_text_after_title = models.TextField(verbose_name='دومین متن مقاله بعد عنوان', null=True, blank=True)
    third_text_after_title = models.TextField(verbose_name='سومین متن مقاله بعد عنوان', null=True, blank=True)
    first_question = models.CharField(verbose_name='اولین سوال', max_length=100, null=True, blank=True)
    first_question_text = models.TextField(verbose_name='اولین متن بعد سوال اول', null=True, blank=True)
    second_title = models.CharField(verbose_name='دومین عنوان', max_length=100, null=True, blank=True)
    second_title_text = models.TextField(verbose_name='دومین متن بعد سوال دوم', null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name='فعال/غیرفعال بودن')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='نویسنده', null=True, editable=False)
    create_date = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='تاریح ثبت')
    category = models.ForeignKey(ArticleCategory, on_delete=models.CASCADE, null=True, blank=True)

    def get_absolute_url_article(self):
        return reverse('article_detail', args=[self.slug])

    def __str__(self):
        return self.title

    def get_jalali_create_date(self):
        return date2jalali(self.create_date)

    def get_jalali_create_time(self):
        return self.create_date.strftime('%H:%M')

    def get_total_likes(self):
        return self.article_likes.users.count()

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'


class ArticleLike(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE, verbose_name='مقاله',
                                   related_name='article_likes')
    users = models.ManyToManyField(User, related_name='article_requirement_comment_likes', verbose_name='کاربران')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.article.title)

    class Meta:
        verbose_name = 'پسندیدن'
        verbose_name_plural = 'لیست پسندیدن'


class ArticleGallery(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE, verbose_name='محصول')
    image = models.ImageField(upload_to='images/article-gallery', verbose_name='تصویر محصولات')


    def __str__(self):
        return self.article.title

    class Meta:
        verbose_name = 'تصویر گالری'
        verbose_name_plural = 'گالری تصاویر'


class ArticleVisit(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='مقاله')
    ip = models.CharField(max_length=30, verbose_name='ای پی کابر')
    user = models.ForeignKey(User, null=True, blank=True, verbose_name='کاربری که مشاهده کرده',
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.article.title

    class Meta:
        verbose_name = 'مشاهده مقاله'
        verbose_name_plural = 'لیست مشاهده مقاله'
