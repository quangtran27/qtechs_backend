# Generated by Django 4.2 on 2023-05-03 04:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_rename_producttype_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='optionimage',
            name='option',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.productoption'),
        ),
    ]
