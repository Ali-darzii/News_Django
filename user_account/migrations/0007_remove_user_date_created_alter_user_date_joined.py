# Generated by Django 4.1.6 on 2023-08-13 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_account', '0006_user_date_created_alter_user_date_joined'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='date_created',
        ),
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='تاریخ ساخت'),
        ),
    ]