from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = (
			'id', 
			'username', 
			'password',
			'first_name', 
			'last_name',
			'phone', 
			'gender', 
			'email', 
			'address',
		)

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].validators = []
