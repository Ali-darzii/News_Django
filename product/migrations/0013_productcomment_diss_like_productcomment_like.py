# Generated by Django 4.1.6 on 2023-09-07 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0012_productcomment_star'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcomment',
            name='diss_like',
            field=models.IntegerField(default=0, verbose_name='نپسندیدن'),
        ),
        migrations.AddField(
            model_name='productcomment',
            name='like',
            field=models.IntegerField(default=0, verbose_name='پسندیدن'),
        ),
    ]
