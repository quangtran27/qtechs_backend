# Generated by Django 4.1.7 on 2023-04-21 03:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("reviews", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Brand",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("image", models.ImageField(upload_to="images/brand/%Y/%m/%D")),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField()),
                (
                    "brand",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="products.brand",
                    ),
                ),
                (
                    "review",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="reviews.review",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Laptop",
            fields=[
                (
                    "product_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="products.product",
                    ),
                ),
                ("logo", models.ImageField(upload_to="images/product/logo/%Y/%m/%D")),
                ("screen", models.FloatField()),
                ("battery", models.CharField(max_length=10)),
            ],
            bases=("products.product",),
        ),
        migrations.CreateModel(
            name="LaptopImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("order", models.PositiveSmallIntegerField()),
                ("image", models.ImageField(upload_to="images/product/%Y/%m/%D")),
                (
                    "laptop",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.laptop",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="LaptopConfig",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ram", models.PositiveSmallIntegerField()),
                ("storage", models.PositiveSmallIntegerField()),
                ("on_sale", models.BooleanField(default=False)),
                ("price", models.PositiveIntegerField()),
                ("sale_price", models.PositiveIntegerField()),
                ("color", models.CharField(max_length=100)),
                ("color_hex", models.CharField(max_length=10)),
                (
                    "laptop",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.laptop",
                    ),
                ),
            ],
        ),
    ]
