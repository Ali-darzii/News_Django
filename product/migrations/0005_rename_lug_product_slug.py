# Generated by Django 4.1.6 on 2023-09-02 08:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_product_inventory_product_inventory_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='lug',
            new_name='slug',
        ),
    ]