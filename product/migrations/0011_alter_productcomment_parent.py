# Generated by Django 4.1.6 on 2023-09-03 20:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_productcomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcomment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.productcomment', verbose_name='والد'),
        ),
    ]