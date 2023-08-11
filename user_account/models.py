from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    avatar = models.ImageField(upload_to='images/profile', blank=True, null=True ,verbose_name='تصویر اواتار')
    address = models.TextField(max_length=200, blank=True, null=True, verbose_name='ادرس')
    about_user = models.TextField(max_length=200, blank=True, null=True, verbose_name='درباره نویسنده')
    email_active_code = models.CharField(max_length=100,verbose_name='کد فعال سازی ایمیل')

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        if self.first_name is not '' and self.last_name is not '':
            return f'{self.first_name} {self.last_name}'
        return self.email
