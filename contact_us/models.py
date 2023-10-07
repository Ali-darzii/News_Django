from django.db import models


# Create your models here.

class ContactUs(models.Model):
    full_name = models.CharField(max_length=200, verbose_name='نام و نام خانوادگی')
    email = models.CharField(max_length=200, verbose_name='ایمیل')
    title = models.CharField(max_length=200, verbose_name='عنوان')
    text_massege = models.TextField(max_length=400, verbose_name='متن درخواست')

    def __str__(self):
        return str(self.full_name)

    class Meta:
        verbose_name = '  فرم تماس با ما'
        verbose_name_plural = 'فرم لیست تماس با ما'


class ContactUsInfo(models.Model):
    right_title = models.CharField(max_length=20, verbose_name='عنوان سمت راست')
    fist_right_text = models.CharField(max_length=120, verbose_name=' اولین متن سمت راست')
    second_right_text = models.CharField(max_length=120, verbose_name='دومین متن سمت راست')
    left_title = models.CharField(max_length=30, verbose_name='عنوان سمت چپ')
    left_text = models.CharField(max_length=120, verbose_name='متن سمت چپ')
    address = models.CharField(max_length=100, verbose_name='ادرس')
    phone_no = models.CharField(max_length=100, verbose_name='تلفن')
    email = models.EmailField(max_length=100, verbose_name='ایمیل')
    work_time = models.TextField(max_length=120, verbose_name='ساعت کاری')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'اطلاعات تماس با ما'
        verbose_name_plural = 'لیست اطلاعات تماس با ما'
