from rest_framework import serializers

from products.serializers import ProductOptionSerializer

from .models import Order, OrderItem


class OrderSerialzier(serializers.ModelSerializer):
	items = serializers.SerializerMethodField()
	created = serializers.SerializerMethodField()
	updated = serializers.SerializerMethodField()
	class Meta:
		model = Order
		fields = (
			'id',
			'user_id',
			'created',
			'updated',
			'status',
			'customer_name',
			'customer_phone',
			'customer_address',
			'payment',
			'shipping_fee',
			'is_paid',
			'is_reviewed',
			'note',
			'total',
			'items'
		)
	def get_items(self, obj):
		return [ OrderItemSerializer(item).data for item in obj.items.all() ]
	def get_created(self, obj):
		return obj.created.strftime("%d/%m/%Y %H:%M")
	def get_updated(self, obj):
		return obj.updated.strftime("%d/%m/%Y %H:%M")

class OrderItemSerializer(serializers.ModelSerializer):
	option = serializers.SerializerMethodField()
	class Meta:
		model = OrderItem
		fields = (
			'option',
			'on_sale',
			'price',
			'sale_price',
			'quantity'
		)
	
	def get_option(self, obj):
		return ProductOptionSerializer(obj.option).data
