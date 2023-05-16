from django.contrib import admin
from nested_admin import NestedModelAdmin, NestedStackedInline

from .models import (
    Brand,
    Category,
    OptionImage,
    OptionSpec,
    Product,
    ProductOption,
    SpecAttribute,
)


class OptionSpecInline(NestedStackedInline):
    model = OptionSpec
    extra = 0

class OptionImageInline(NestedStackedInline):
    model = OptionImage
    extra = 0

class ProductOptionAdmin(NestedStackedInline):
    model = ProductOption
    extra = 0
    inlines = [OptionSpecInline, OptionImageInline]

class ProductAdmin(NestedModelAdmin):
    model = Product
    inlines = [ProductOptionAdmin]


admin.site.register(Product, ProductAdmin)
admin.site.register(Brand)
admin.site.register(SpecAttribute)
admin.site.register(Category)
