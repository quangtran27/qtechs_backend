from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Brand, Product
from .serializers import BrandSerializer, ProductImageSerializer

PRODUCTS_PER_PAGE = 20

@api_view(['GET'])
def get_all_brands(request):
    type = request.GET.get('type', 'product')
    brands = []
    if type == 'product':
        brands = Brand.objects.filter(product__isnull=False).distinct()
    elif type == 'laptop':
        brands = Brand.objects.filter(product__laptop__isnull=False).distinct()
    serializer = BrandSerializer(brands, many=True)
    return Response(serializer.data, status.HTTP_200_OK)


    

@api_view(['GET'])
def get_product_images(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
        images = product.images.all()
        serializer = ProductImageSerializer(images, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    except Product.DoesNotExist as e:
        print(e)
        return Response([], status.HTTP_404_NOT_FOUND)