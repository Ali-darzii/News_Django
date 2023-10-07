from django.db import models


class Expert(models.Model):
    full_name = models.CharField(max_length=30, verbose_name='اسم و فامیلی')
    image = models.ImageField(upload_to='images/expert', verbose_name='عکس')
    roll = models.CharField(max_length=30, verbose_name='نقش')
    email = models.EmailField(max_length=40, null=True, blank=True, verbose_name='ایمیل')
    face_book = models.CharField(max_length=70, null=True, blank=True, verbose_name='فیس بوک')
    twitter = models.CharField(max_length=70, null=True, blank=True, verbose_name='تویتر')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'کارشناس'
        verbose_name_plural = 'کارشناسان'


class AboutUs(models.Model):
    head_image = models.ImageField(upload_to='images/about_us', verbose_name='عکس سر تیتر')
    first_title = models.CharField(max_length=20, null=True, blank=True, verbose_name='عنوان اول')
    first_text = models.TextField(null=True, blank=True, verbose_name='متن اول')
    second_title = models.CharField(max_length=20, null=True, blank=True, verbose_name='عنوان دوم')
    first_goal_text = models.TextField(null=True, blank=True, verbose_name='متن طبقه بندی شده اول')
    second_goal_text = models.TextField(null=True, blank=True, verbose_name='متن طبقه بندی شده سوم')
    third_goal_text = models.TextField(null=True, blank=True, verbose_name='متن طبقه بندی شده سوم')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.first_title

    class Meta:
        verbose_name = 'درباره ما'
        verbose_name_plural = 'لیست درباره ما'
