# Generated by Django 4.1.7 on 2023-05-02 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='priority',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='productoption',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productoption',
            name='sold',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
