# Generated by Django 4.1.6 on 2023-09-27 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('about_us', '0004_remove_about_us_second_text_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='About_Us',
            new_name='AboutUs',
        ),
        migrations.AlterField(
            model_name='expert',
            name='full_name',
            field=models.CharField(max_length=30, verbose_name='اسم و فامیلی'),
        ),
    ]