from django.core.paginator import Paginator
from django.db.models import Min, Q, Sum
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Brand, Category, Product
from .serializers import BrandSerializer, CategorySerializer, ProductSerializer

PAGE_SIZE = 20

@api_view(['GET'])
def get_all_brands(request):
	brands = Brand.objects.all()
	return Response(BrandSerializer(brands, many=True).data, status.HTTP_200_OK)

@api_view(['GET'])
def get_brand(request, brand_id):
	try:
		brand = Brand.objects.get(id=brand_id)
		return Response(BrandSerializer(brand).data, status.HTTP_200_OK)
	except:
		return Response({}, status.HTTP_404_NOT_FOUND) 

@api_view(['GET'])
def get_all_categories(request):
	types = Category.objects.all().order_by('order')
	return Response(CategorySerializer(types, many=True).data, status.HTTP_200_OK)

@api_view(['GET'])
def get_category(request, category_id):
	try:
		category = Category.objects.get(id=category_id)
		return Response(CategorySerializer(category).data, status.HTTP_200_OK)
	except:
		return Response({}, status.HTTP_404_NOT_FOUND) 
	

@api_view(['GET'])
def get_all_products(request):
	page = request.GET.get('page')
	page_size = request.GET.get('pageSize', PAGE_SIZE)
	sort_by = request.GET.get('sort_by', '')
	brands = request.GET.get('brands', '').split('|')
	order = request.GET.get('order', '')
	type = request.GET.get('category', 'laptop')

	try:
		products = Product.objects.filter(category__path=type)
	except:
		return Response({}, status.HTTP_400_BAD_REQUEST)


	if len(brands) > 1:
		products = products.filter(brand__name__in=brands)
	if sort_by == 'price':
		products = products.annotate(min_price=Min('productoptionset__sale_price', filter=Q(productoption__on_sale=True))).order_by('min_price')
	if order == 'desc':
		products = products.reverse()

	products.distinct()
		
	# Paging
	if page is not None:
		try:
			paginator = Paginator(products, page_size)
			page = (int) (page)
			page_size = (int) (page_size)
			if page > paginator.num_pages or page < 1: page = 1
			paginated_products = paginator.page(page)
			return Response({
					'data': ProductSerializer(paginated_products, many=True).data,
					'paging': {
							'page': page,
							'page_size': page_size,
							'total': paginator.count,
					}
			}, status.HTTP_200_OK)

		except:
			return Response({}, status.HTTP_400_BAD_REQUEST)
	else:
		return Response(ProductSerializer(products, many=True).data, status.HTTP_200_OK)


@api_view(['GET'])
def get_product(request, product_id):
	try:
		product = Product.objects.get(id=product_id)
		return Response(ProductSerializer(product).data, status.HTTP_200_OK)
	except Product.DoesNotExist:
		return Response({}, status.HTTP_404_NOT_FOUND) 

@api_view(['GET'])
def get_product_name(request, product_id):
	try:
		product = Product.objects.get(id=product_id)
		return Response({'name': product.name}, status.HTTP_200_OK)
	except Product.DoesNotExist:
		return Response({}, status.HTTP_404_NOT_FOUND)