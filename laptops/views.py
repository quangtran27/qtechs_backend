from django.core.paginator import Paginator
from django.db.models import Min, Q, Sum
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from products.models import Brand
from products.serializers import BrandSerializer

from .models import Laptop, LaptopConfig
from .serializers import LaptopConfigSerializer, LaptopSerializer

PAGE_SIZE = 20

@api_view(['GET'])
def get_all_laptops(request):
    # params for paging
    page = request.GET.get('page')
    page_size = request.GET.get('pageSize', PAGE_SIZE)
    limit = request.GET.get('limit', PAGE_SIZE)
    offset = request.GET.get('offset')

    # params for sort
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
        laptops = laptops.annotate(min_price=Min('configs__sale_price', filter=Q(laptopconfig__on_sale=True))).order_by('min_price')
    elif sort_by == 'sold':
        laptops = laptops.annotate(total_sold=Sum('configs__sold')).order_by('-total_sold')
    else:
        laptops = laptops.annotate(total_sold=Sum('configs__sold')).order_by('-id')

    if page is not None or page_size is not None or limit is not None or offset: # paging or limit
        # Paging:
        if page is not None and page_size is not None:
            try:
                page = (int) (page)
                page_size = (int) (page_size)
                paginator = Paginator(laptops, page_size)
                if page > paginator.num_pages or page < 1: page = 1
                paginated_laptops = paginator.page(page)
                return Response({
                    'data': LaptopSerializer(paginated_laptops, many=True).data,
                    'paging': {
                        'page': page,
                        'page_size': page_size,
                        'total': paginator.count,
                    }
                }, status.HTTP_200_OK)
            except Exception as e:
                print(e)
                print(page, page_size)
                return Response({}, status.HTTP_400_BAD_REQUEST)
        else: # limit:
            return Response({
                'data': [],
                'paging': {
                    'limit': 0,
                    'offset': 0,
                    'total': 0
                }
            })
    else: # do not paging or limit
        serializer = LaptopSerializer(laptops, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
        
@api_view(['GET'])
def get_laptop(request, laptop_id):
    try:
        laptop = Laptop.objects.get(id=laptop_id)
        return Response(LaptopSerializer(laptop).data, status.HTTP_200_OK)
    except Laptop.DoesNotExist:
        return Response({}, status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_laptop_configs(request, laptop_id):
    try:
        laptop = Laptop.objects.get(pk=laptop_id)
        configs = laptop.configs.all()
        serializer = LaptopConfigSerializer(configs, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    except Laptop.DoesNotExist :
        return Response([], status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def get_all_laptop_brands(request):
    brands = Brand.objects.filter(product__laptop__isnull=False).distinct()
    serializer = BrandSerializer(brands, many=True)
    return Response(serializer.data, status.HTTP_200_OK)
