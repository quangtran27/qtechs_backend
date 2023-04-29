from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User
from .serialziers import UserLoginSerializer, UserSerializer


def get_serializer_errors(serializer):
    errors = []
    for field, error_list in serializer.errors.items():
        for error in error_list:
            errors.append(f"{error}")
    return "\n ".join(errors)

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        errors = get_serializer_errors(serializer)
        return Response({"error_message": errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.get(phone=serializer.validated_data['phone'])
        if user and user.password == serializer.validated_data['password']:
            refresh = TokenObtainPairSerializer.get_token(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            access_expires = int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds())
            refresh_expires = int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds())
            user_data = UserSerializer(user).data
            return Response({
                'access_token': access_token,
                'refresh_token': refresh_token,
                'access_expires': access_expires,
                'refresh_expires': refresh_expires,
                'user': user_data
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error_message': 'Đăng nhập thất bại! Số điện thoại hoặc mật khẩu không chính xác.'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)