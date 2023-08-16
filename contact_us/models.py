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
        verbose_name = 'تماس با ما'
        verbose_name_plural = 'لیست تماس با ما'
