from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Cart, CartItem
from .serializers import CartItemSerializer, CartSerializer


@api_view(['GET'])
def get_cart(request, cart_id):
    try:
        cart = Cart.objects.get(id=cart_id)
        return Response(CartSerializer(cart).data, status.HTTP_200_OK)
    except Cart.DoesNotExist:
        return Response({}, status.HTTP_404_NOT_FOUND)