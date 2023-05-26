from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from promotions.models import Banner
from promotions.serializers import BannerSerializer


@api_view(['GET'])
def get_all_banners(request):
  banners = Banner.objects.all().order_by('order')
  return Response(BannerSerializer(banners, many=True).data, status.HTTP_200_OK)