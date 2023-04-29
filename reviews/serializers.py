from rest_framework import serializers

from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()
    class Meta:
        model = Review
        fields = [
            'id',
            'user_id',
            'title',
            'body',
            'created',
            'updated',
        ]
    def get_user_id(self, obj):
        return obj.user.id