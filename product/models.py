from django.db import models

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
    lug = models.SlugField(default="", null=False, db_index=True, blank=True, max_length=200, unique=True,
                           verbose_name='عنوان در url')
    is_delete = models.BooleanField(verbose_name='حذف شده / نشده')
    category = models.ManyToManyField(
        ProductCategory,
        related_name="product_categories",
        verbose_name='دسته بندی ها')
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE, verbose_name='برند', null=True, blank=True)

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