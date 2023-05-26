from rest_framework import serializers

from .models import Brand, Category, OptionSpec, Product, ProductOption


class BrandSerializer(serializers.ModelSerializer):
	class Meta:
		model = Brand
		fields = [ 'id', 'name', 'image' ]

class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = [ 'id', 'name', 'image' ]
    
class ProductSerializer(serializers.ModelSerializer):
	options = serializers.SerializerMethodField()
	class Meta:
		model = Product
		fields = [ 'id', 'name', 'category_id', 'brand_id', 'status', 'review_id', 'options' ]
	def get_options(self, obj):
		return ProductOptionSerializer(obj.productoption_set.all(), many=True).data

class ProductOptionSerializer(serializers.ModelSerializer):
	images = serializers.SerializerMethodField()
	specs = serializers.SerializerMethodField()
	name = serializers.SerializerMethodField()

	class Meta:
		model = ProductOption
		fields = ['id', 'name', 'SKU', 'on_sale', 'price', 'sale_price', 'sold', 'quantity', 'color', 'summary', 'specs', 'images']

	def get_images(self, obj):
		return [ image.image.url for image in obj.optionimage_set.all() ]
	def get_specs(self, obj):
		return OptionSpecSerializer(obj.optionspec_set.all(), many=True).data
	def get_name(self, obj):
		return obj.product.name
	
class OptionSpecSerializer(serializers.ModelSerializer):
	name = serializers.SerializerMethodField()
	code = serializers.SerializerMethodField()
	class Meta:
		model = OptionSpec
		fields = [ 'name', 'code', 'value' ]
		depth = 1
	def get_name(self, obj):
		return obj.attr.name
	def get_code(self, obj):
		return obj.attr.code