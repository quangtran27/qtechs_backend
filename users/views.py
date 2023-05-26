from itertools import product
from multiprocessing import Value
from statistics import quantiles

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from carts.models import Cart, CartItem
from carts.serializers import CartItemSerializer, CartSerializer
from orders.models import Order, OrderItem
from orders.serializers import OrderSerialzier
from products.models import ProductOption
from users import serialziers

from .models import User
from .serialziers import UserLoginSerializer, UserSerializer


def get_serializer_errors(serializer):
	errors = []
	for _, error_list in serializer.errors.items():
		for error in error_list:
			errors.append(f"{error}")
	return "\n".join(errors)

@api_view(['POST'])
def register(request):
	serializer = UserSerializer(data=request.data)
	if serializer.is_valid():
		serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
		serializer.save()
		serializer.validated_data['password'] = ''
		return Response(serializer.data, status.HTTP_201_CREATED)
	else:
		errors = get_serializer_errors(serializer)
		return Response({"error_message": errors}, status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
	serializer = UserLoginSerializer(data=request.data)
	if serializer.is_valid():
		user = authenticate(
				request,
				username=serializer.validated_data['username'],
				password=serializer.validated_data['password']
		)
		if user:
			refresh = TokenObtainPairSerializer.get_token(user)
			access_token = str(refresh.access_token)
			refresh_token = str(refresh)
			return Response({
				'access_token': access_token,
				'refresh_token': refresh_token,
				'user_id': user.id,
			}, status.HTTP_200_OK)
		else:
			return Response({
					'error_message': 'Đăng nhập thất bại! Số điện thoại hoặc mật khẩu không chính xác.'
				}, status.HTTP_401_UNAUTHORIZED)
	else:
		return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
	
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def get_or_update_user_info(request, user_id):
	try:
		user = User.objects.get(id=user_id)
	except User.DoesNotExist:
		return Response({}, status.HTTP_404_NOT_FOUND)
	
	if request.method == 'GET':
		user.password = ''
		return Response(UserSerializer(user).data, status.HTTP_200_OK)
	else:
		name = request.POST.get('name')
		phone = request.POST.get('phone')
		gender = request.POST.get('gender')
		email = request.POST.get('email')
		address = request.POST.get('address')
		image = request.FILES.get('image')

		if name:
			user.name = name
		if phone:
			user.phone = phone
		if gender:
			try:
				gender = (int) (gender)
				if gender != 1 and gender != 2 and gender != 3:
					raise ValueError
				user.gender = gender
			except ValueError as e:
				return Response({}, status.HTTP_400_BAD_REQUEST)
		if email:
			user.email = email
		if address:
			user.address = address
		if image:
			user.image = image
			
		user.save()
		return Response(UserSerializer(user).data, status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_cart(request, user_id):
	try:
		user = User.objects.get(id=user_id)
	except User.DoesNotExist:
		return Response({}, status.HTTP_404_NOT_FOUND) 
	cart, _ = Cart.objects.get_or_create(user=user)
	return Response(CartSerializer(cart).data, status.HTTP_200_OK)
	
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request, user_id):
	option_id = (int) (request.POST.get('option_id', '0'))
	quantity = (int) (request.POST.get('quantity', '0'))

 	# Validate params
	if option_id <= 0 or quantity <= 0:
		return Response({}, status.HTTP_400_BAD_REQUEST) 
	
	# Check resource
	try:
		user = User.objects.get(id=user_id)
		option = ProductOption.objects.get(id=option_id)
		if option.product.status == False: 
			raise ProductOption.DoesNotExist
	except (User.DoesNotExist, ProductOption.DoesNotExist):
		return Response({}, status.HTTP_404_NOT_FOUND) 
	
	cart, _ = Cart.objects.get_or_create(user=user)
	cart_item, is_cart_item_created = CartItem.objects.get_or_create(cart=cart, option=option)
	if is_cart_item_created:
		if quantity <= option.quantity:
			cart_item.quantity = quantity
		else:
			return Response({}, status.HTTP_400_BAD_REQUEST) 
	else:
		if cart_item.quantity + quantity <= option.quantity:
			cart_item.quantity += quantity
		else:
			return Response({}, status.HTTP_400_BAD_REQUEST) 
	cart_item.save()

	return Response(CartItemSerializer(cart_item).data, status.HTTP_200_OK)
	
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def update_or_delete_cart_item(request, user_id, cart_item_id):
	try:
		User.objects.get(id=user_id)
		cart_item = CartItem.objects.get(id=cart_item_id)
	except (User.DoesNotExist, CartItem.DoesNotExist):
		return Response({}, status.HTTP_404_NOT_FOUND)
	
	if request.method == 'PUT':
		quantity = request.POST.get('quantity')
		try:
			quantity = (int) (quantity)
			if quantity <= 0: raise ValueError
		except ValueError:
			return Response({
				'message': 'Dữ liệu không hợp lệ'
			}, status.HTTP_400_BAD_REQUEST)
		if quantity > cart_item.option.quantity:
			return Response({'message': f'Rất tiếc, bạn chỉ có thể mua tối đa {cart_item.quantity} sản phẩm của mặt hàng này'}, status.HTTP_400_BAD_REQUEST)
		
		cart_item.quantity = quantity
		cart_item.save()
		return Response(CartItemSerializer(cart_item).data, status.HTTP_200_OK)
	else:
		cart_item.delete()
		return Response({}, status.HTTP_204_NO_CONTENT)

PAGE_SIZE = 6
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_orders_add_order(request, user_id):
	try:
		user = User.objects.get(id=user_id)
	except User.DoesNotExist:
		return Response({}, status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		page = request.GET.get('page')
		page_size = request.GET.get('page_size', PAGE_SIZE)
		orders = Order.objects.filter(user=user).order_by('-id')

		if page is not None:
			try:
				page = int(page)
				page_size = int(page_size)
				paginator = Paginator(orders, page_size)
				if page < 1: raise ValueError
				if page > paginator.num_pages:
					paginated_orders = []
				else:
					paginated_orders = paginator.page(page)
				return Response({
					'data': OrderSerialzier(paginated_orders, many=True).data,
					'paging': {
							'page': page,
							'page_size': page_size,
							'total': paginator.count,
					}
			}, status.HTTP_200_OK)
			except:
				return Response({}, status.HTTP_400_BAD_REQUEST)
					
		else:
			return Response(OrderSerialzier(orders, many=True).data, status.HTTP_200_OK)
	

	else:
		customer_name = request.POST.get('customer_name')
		customer_phone = request.POST.get('customer_phone')
		customer_address = request.POST.get('customer_address')
		payment = request.POST.get('payment')
		note = request.POST.get('note')
		cart_item_ids = request.POST.get('cart_item_ids')
		order_status = 1
		is_paid = False
		total = 0
		# Check if any required data is empty
		if (customer_name is None) or (customer_phone is None) or (customer_address is None) or (payment is None) or (cart_item_ids is None):
			return Response({}, status.HTTP_400_BAD_REQUEST)
		try:
			# Validate 
			payment = (int) (payment)
			if payment != 1 and payment != 2:
				raise ValueError
			
			# Check if any order items does not belong to user or has invalid quantity
			cart_item_ids = cart_item_ids.split(',')
			for cart_item_id in cart_item_ids:
				cart_item = CartItem.objects.get(pk=cart_item_id)
				option = cart_item.option
				if cart_item.quantity > option.quantity or cart_item.cart.user.id != user_id:
					raise ValueError
		except CartItem.DoesNotExist:
			return Response({}, status.HTTP_404_NOT_FOUND)
		except Exception as e:
			print(e)
			return Response({}, status.HTTP_400_BAD_REQUEST)
		
		order = Order(
			user=user,
			status=order_status,
			customer_name=customer_name,
			customer_phone=customer_phone,
			customer_address=customer_address,
			payment=payment,
			is_paid=is_paid,
			note=note,
			total=total
		)
		order.save()

		for id in cart_item_ids:
			cart_item = CartItem.objects.get(id=id)
			option = cart_item.option
			order_item = OrderItem(
				order=order,
				option=option,
				on_sale=option.on_sale,
				price=option.price,
				sale_price=option.sale_price,
				quantity=cart_item.quantity
			)
			order_item.save()

			option.quantity -= order_item.quantity
			option.sold += order_item.quantity
			option.save()

			order.total += (order_item.sale_price if order_item.on_sale else order_item.price) * order_item.quantity
			order.save()
			cart_item.delete()
			
		if order.total < 500000:
			order.shipping_fee = 70000
			order.save()
		return Response(OrderSerialzier(order).data, status.HTTP_201_CREATED)
		

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_password(request, user_id):
	try:
		_user = User.objects.get(id=user_id)
	except User.DoesNotExist:
		return Response({}, status.HTTP_404_NOT_FOUND)
	
	old_password = request.POST.get('old_password')
	new_password = request.POST.get('new_password')

	if old_password == new_password:
		return Response({'message': 'Mật khẩu mới không được giống với mật khẩu hiện tại'})

	user = authenticate(username=_user.username, password=old_password)

	if user is not None:
		user.set_password(new_password)
		user.save()
		return Response({}, status.HTTP_200_OK)

	else:
		return Response({'message': 'Mật khẩu chưa chính xác'}, status.HTTP_401_UNAUTHORIZED)