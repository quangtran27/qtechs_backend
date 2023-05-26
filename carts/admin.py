from django.contrib import admin
from nested_admin import NestedModelAdmin, NestedStackedInline

from .models import Cart, CartItem


class CartIemInline(NestedStackedInline):
	model = CartItem
	extra = 0

class CartAdmin(NestedModelAdmin):
	model = Cart
	inlines = [CartIemInline]
	
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)
