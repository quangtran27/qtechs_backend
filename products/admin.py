from django.contrib import admin
from nested_inline.admin import NestedModelAdmin, NestedStackedInline

from .models import Brand, Laptop, LaptopConfig, ProductImage


class LaptopConfigInline(NestedStackedInline):
    model = LaptopConfig
    extra = 0
    fk_name = 'laptop'

class ProductImageInline(NestedStackedInline):
    model = ProductImage
    extra = 0
    fk_name = 'product'

class LaptopAdmin(NestedModelAdmin):
    model = Laptop
    inlines = [ LaptopConfigInline, ProductImageInline ]

admin.site.register(Brand)
admin.site.register(Laptop, LaptopAdmin)
