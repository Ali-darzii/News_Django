from django.db import models
from django.db.models import Avg
from django.urls import reverse
from user_account.models import User


class ProductCategory(models.Model):
    title = models.CharField(max_length=300, db_index=True, verbose_name='عنوان')
    urls_title = models.CharField(max_length=300, db_index=True, verbose_name='عنوان در url')
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال')
    is_delete = models.BooleanField(verbose_name='حذف شده / نشده')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"


class ProductBrand(models.Model):
    title = models.CharField(max_length=300, verbose_name='نام برند', db_index=True)
    url_title = models.CharField(max_length=200, unique=True, verbose_name='نام در url', db_index=True)
    is_active = models.BooleanField(verbose_name='فعال/غیر فعال')

    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برند ها'

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=300, verbose_name='نام محصول')
    image = models.ImageField(upload_to='images/products', null=True, blank=True, verbose_name='تصویر محصول')
    price = models.IntegerField(verbose_name='قیمت')
    short_descriptions = models.CharField(max_length=360, null=True, db_index=True, verbose_name='توضیحات کوتاه')
    descriptions = models.TextField(verbose_name='توضیحات اصلی', db_index=True)
    is_active = models.BooleanField(default=False, verbose_name='فعال/غیر فعال')
    slug = models.SlugField(default="", null=False, db_index=True, blank=True, max_length=200, unique=True,
                            verbose_name='عنوان در url')
    is_delete = models.BooleanField(verbose_name='حذف شده / نشده')
    category = models.ManyToManyField(
        ProductCategory,
        related_name="product_categories",
        verbose_name='دسته بندی ها')
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE, verbose_name='برند', null=True, blank=True)
    inventory = models.BooleanField(verbose_name='موحودی', default=True)
    inventory_number = models.IntegerField(verbose_name='تعداد کالا')
    weight = models.CharField(max_length=100, verbose_name='وزن', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])

    def int_star_average(self):
        star = self.productcomment_set.filter(product_id=self.id).aggregate(Avg('star'))['star__avg']
        if star is None:
            star = 3
        return range(int(star))

    def half_star_average(self):
        star = self.productcomment_set.filter(product_id=self.id).aggregate(Avg('star'))['star__avg']
        half_star = False
        if star is None:
            star = 3
        else:
            round(star, 1)
            if int(star * 10) % 10 != 0:
                half_star = True
        return half_star

    def __str__(self):
        return f"{self.title} "

    class Meta:
        verbose_name = "محصول"  #
        verbose_name_plural = "محصولات"


class ProductTag(models.Model):
    caption = models.CharField(max_length=200, db_index=True, verbose_name='عنوان')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products_tags',
                                verbose_name='تگ محصول')

    class Meta:
        verbose_name = "تگ محصول"
        verbose_name_plural = "تگ های محصولات"

    def __str__(self):
        return self.caption


class ProductVisit(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    ip = models.CharField(max_length=30, verbose_name='ای پی کابر')
    user = models.ForeignKey(User, null=True, blank=True, verbose_name='کاربری که مشاهده کرده',
                             on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.title} / {self.ip}"

    class Meta:
        verbose_name = 'بازدید محصول'
        verbose_name_plural = 'بازدیدهای محصول'


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    image = models.ImageField(upload_to='images/product-gallery', verbose_name='تصویر محصولات')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'تصویر گالری'
        verbose_name_plural = 'گالری تصاویر'


class ProductComment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    parent = models.ForeignKey('ProductComment', on_delete=models.CASCADE, blank=True, null=True, verbose_name='والد')
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE, verbose_name='کاربر')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
    comment = models.TextField(verbose_name='متن نظر')
    star = models.IntegerField(verbose_name='ستاره')
    like = models.IntegerField(verbose_name='پسندیدن', default=0)
    diss_like = models.IntegerField(verbose_name='نپسندیدن', default=0)

    def get_total_likes(self):
        return self.likes.users.count()

    def get_total_dis_like(self):
        return self.dis_likes.users.count()

    def __str__(self):
        return str(self.comment)[:30]

    class Meta:
        verbose_name = 'نظر محصول'
        verbose_name_plural = 'نظرات محصول'


class Like(models.Model):
    comment = models.OneToOneField(ProductComment, on_delete=models.CASCADE, related_name='likes',
                                   verbose_name='پسندیدن')
    users = models.ManyToManyField(User, related_name='requirement_comment_likes', verbose_name='کاربران')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.comment.comment)[:30]

    class Meta:
        verbose_name = 'پسندیدن'
        verbose_name_plural = 'لیست پسندیدن'


class DisLike(models.Model):
    comment = models.OneToOneField(ProductComment, on_delete=models.CASCADE, related_name='dis_likes',
                                   verbose_name='نپسندیدن')
    users = models.ManyToManyField(User, related_name='requirement_comment_dis_likes', verbose_name='کاربران')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.comment.comment)[:30]

    class Meta:
        verbose_name = 'نپسندیدن'
        verbose_name_plural = 'لیست نپسندیدن'
