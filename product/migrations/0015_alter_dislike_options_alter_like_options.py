# Generated by Django 4.1.6 on 2023-09-13 11:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_rename_text_productcomment_comment_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dislike',
            options={'verbose_name': 'نپسندیدن', 'verbose_name_plural': 'لیست نپسندیدن'},
        ),
        migrations.AlterModelOptions(
            name='like',
            options={'verbose_name': 'پسندیدن', 'verbose_name_plural': 'لیست پسندیدن'},
        ),
    ]
