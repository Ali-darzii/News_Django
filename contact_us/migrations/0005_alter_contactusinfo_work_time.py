# Generated by Django 4.1.6 on 2023-09-27 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact_us', '0004_alter_contactus_options_contactusinfo_is_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactusinfo',
            name='work_time',
            field=models.TextField(max_length=120, verbose_name='ساعت کاری'),
        ),
    ]
