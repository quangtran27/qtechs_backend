# Generated by Django 4.2 on 2023-05-02 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_priority_productoption_quantity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productoption',
            name='summary',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
