# Generated by Django 2.2 on 2019-04-20 13:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parse', '0002_products'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Products',
            new_name='Product',
        ),
        migrations.RenameModel(
            old_name='Sellers',
            new_name='Seller',
        ),
    ]
