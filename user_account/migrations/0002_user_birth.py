# Generated by Django 4.1.6 on 2023-08-11 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='birth',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='تولد'),
        ),
    ]
