from multiprocessing import Value

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from carts.models import Cart, CartItem
from carts.serializers import CartItemSerializer, CartSerializer
from products.models import ProductOption

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
	print('data: ', request.POST)
	option_id = (int) (request.POST.get('option_id', '0'))
	quantity = (int) (request.POST.get('quantity', '0'))

 	# Validate params
	if option_id <= 0 or quantity <= 0:
		print(option_id, quantity)
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
		cart_item.quantity = quantity
	else:
		cart_item.quantity += quantity
	cart_item.save()

	return Response(CartItemSerializer(cart_item).data, status.HTTP_200_OK)
	
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def update_or_delete_cart_item(request, user_id, cart_item_id):
	try:
		user = User.objects.get(id=user_id)
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