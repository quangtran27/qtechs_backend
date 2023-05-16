from rest_framework import serializers

from products.models import ProductOption
from products.serializers import ProductOptionSerializer

from .models import Cart, CartItem


class CartSerializer(serializers.ModelSerializer):
    cart_items = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ['id', 'user_id', 'cart_items']

    def get_cart_items(self, obj):
        _cart_items = obj.cartitem_set.all()
        serializer = CartItemSerializer(_cart_items, many=True)
        return serializer.data
    
class CartItemSerializer(serializers.ModelSerializer):
    option = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields = [ 
            'id', 
            'cart_id',
            'option',
            'quantity'
        ]
    def get_option(self, obj):
        return ProductOptionSerializer(ProductOption.objects.get(id=obj.option.id)).data