from django.db import models


class Slider(models.Model):
    image = models.ImageField(upload_to='images/slider', verbose_name='عکس اسلایدر')
    title = models.CharField(max_length=50, verbose_name='عنوان')
    text = models.TextField(verbose_name='متن')
    date = models.DateField(verbose_name='ناریخ ساخت')
    link = models.CharField(max_length=60, verbose_name='لینک')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'اسلایدر'
        verbose_name_plural = 'اسلایدر ها'

