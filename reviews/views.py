from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Review
from .serializers import ReviewSerializer


@api_view(['GET'])
def get_review(request, review_id):
    try:
        review = Review.objects.get(pk=review_id)
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Review.DoesNotExist as e:
        print(e)
        return Response([], status=status.HTTP_404_NOT_FOUND)