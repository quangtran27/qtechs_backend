# Generated by Django 4.2.1 on 2023-05-23 17:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_alter_optionimage_option'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='path',
        ),
        migrations.AlterField(
            model_name='category',
            name='id',
            field=models.CharField(max_length=100, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator('^[a-zA-Z\\-]+$')]),
        ),
    ]