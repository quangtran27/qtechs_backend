from rest_framework import serializers

from reviews.models import Review

from .models import Brand, Laptop, LaptopConfig, ProductImage


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = [ 'id', 'name', 'image' ]

class LaptopSerializer(serializers.ModelSerializer):
    product_ptr_id = serializers.SerializerMethodField()
    brand_id = serializers.SerializerMethodField()
    review_id = serializers.SerializerMethodField()

    class Meta:
        model = Laptop
        fields = [ 'id', 'product_ptr_id', 'name', 'brand_id', 'review_id' ]

    def get_product_ptr_id(self, obj):
        return obj.product_ptr_id
    def get_brand_id(self, obj):
        return obj.brand.id
    def get_review_id(self, obj):
        return obj.review.id if obj.review else 0
    
class LaptopConfigSerializer(serializers.ModelSerializer):
    laptop_id = serializers.SerializerMethodField()
    class Meta:
        model = LaptopConfig
        fields = [ 
            'id', 
            'laptop_id', 
            'screen', 
            'battery', 
            'cpu', 
            'gpu', 
            'ram', 
            'storage', 
            'quantity', 
            'sold', 
            'on_sale', 
            'price', 
            'sale_price', 
            'color',
        ]
    def get_laptop_id(self, obj):
        return obj.laptop.id

class ProductImageSerializer(serializers.ModelSerializer):
    product_id = serializers.SerializerMethodField()
    class Meta:
        model = ProductImage
        fields = [ 'id', 'product_id', 'order', 'image' ]
    def get_product_id(self, obj):
        return obj.product.id