# Generated by Django 4.1.6 on 2023-08-16 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_account', '0008_alter_user_date_joined'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='post_cart',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='تلفن خانه'),
        ),
    ]
