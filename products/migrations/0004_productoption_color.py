# Generated by Django 4.2 on 2023-05-02 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_productoption_summary'),
    ]

    operations = [
        migrations.AddField(
            model_name='productoption',
            name='color',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]