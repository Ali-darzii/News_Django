from django.db import models
from django.contrib.auth.models import AbstractUser
from jalali_date import date2jalali


# Create your models here.
class User(AbstractUser):
    avatar = models.ImageField(upload_to='images/profile', blank=True, null=True, verbose_name='تصویر اواتار')
    about_user = models.TextField(max_length=200, blank=True, null=True, verbose_name='درباره نویسنده')
    email_active_code = models.CharField(max_length=100, verbose_name='کد فعال سازی ایمیل')
    birth = models.CharField(max_length=20, verbose_name='تولد', blank=True, null=True)
    city = models.CharField(max_length=20, verbose_name='شهر', blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='تاریخ ساخت')

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        if self.first_name != '' and self.last_name != '':
            return f'{self.first_name} {self.last_name}'
        return self.email

    def get_jalali_create_date(self):
        return date2jalali(self.date_joined)

    def get_jalali_create_time(self):
        return self.date_joined.strftime('%H:%M')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=11, blank=True, null=True, verbose_name='تلفن همراه')
    home_phone = models.CharField(max_length=11, blank=True, null=True, verbose_name='تلفن خانه')
    address = models.TextField(max_length=200, blank=True, null=True, verbose_name='ادرس')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'پروفایل'
        verbose_name_plural = 'پروفایل ها'
