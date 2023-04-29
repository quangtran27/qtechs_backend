from django.core.paginator import Paginator
from django.db.models import Min, Q, Sum
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Brand, Laptop, LaptopConfig, Product
from .serializers import (
    BrandSerializer,
    LaptopConfigSerializer,
    LaptopSerializer,
    ProductImageSerializer,
)

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
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_all_laptops(request):
    page = (int) (request.GET.get('page', '1'))
    sort_by = request.GET.get('sort_by', '')
    brands = request.GET.get('brand', '').split('|')
    prices = request.GET.get('price', '').split('|')
    cpus = request.GET.get('cpu', '').split('|')
    rams = request.GET.get('ram', '').split('|')
    
    laptops = Laptop.objects.all()

    # Filter
    if len(brands) > 1:
        laptops = laptops.filter(brand__name__in=brands)
    if len(prices) > 1:
        for price_range in prices:
            price_min, price_max = price_range.split('-')
            laptops = laptops.filter(laptopconfig__price__gte=price_min, laptopconfig__price__lte=price_max)
    if len(cpus) > 1:
        laptops = laptops.filter(laptopconfig__cpu__in=cpus)
    if len(rams) > 1:
        laptops = laptops.filter(laptopconfig__ram__in=rams)
    if sort_by == 'price':
        laptops = laptops.annotate(min_price=Min('laptopconfig__sale_price', filter=Q(laptopconfig__on_sale=True))).order_by('min_price')
    elif sort_by == 'sold':
        laptops = laptops.annotate(total_sold=Sum('laptopconfig__sold')).order_by('-total_sold')

    # Paging
    paginator = Paginator(laptops, PRODUCTS_PER_PAGE)
    if page > paginator.num_pages or page < 1: page = 1
    paginated_laptops = paginator.page(page)

    serializer = LaptopSerializer(paginated_laptops, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_laptop_configs(request, laptop_id):
    try:
        laptop = Laptop.objects.get(pk=laptop_id)
        configs = laptop.configs.all()
        serializer = LaptopConfigSerializer(configs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Laptop.DoesNotExist as e:
        print(e)
        return Response([], status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
def get_product_images(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
        images = product.images.all()
        serializer = ProductImageSerializer(images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Product.DoesNotExist as e:
        print(e)
        return Response([], status=status.HTTP_404_NOT_FOUND)