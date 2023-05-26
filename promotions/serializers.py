from rest_framework import serializers

from promotions.models import Banner


class BannerSerializer(serializers.ModelSerializer):
  class Meta:
    model = Banner
    fields = ('image', 'url')