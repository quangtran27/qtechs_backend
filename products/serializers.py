from rest_framework import serializers

from reviews.models import Review

from .models import Brand, ProductImage


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = [ 'id', 'name', 'image' ]

class ProductImageSerializer(serializers.ModelSerializer):
    product_id = serializers.SerializerMethodField()
    class Meta:
        model = ProductImage
        fields = [ 'id', 'product_id', 'order', 'image' ]
    def get_product_id(self, obj):
        return obj.product.id