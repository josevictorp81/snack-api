from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        read_only = ['id']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 6}}
    
    # def validate(self, attrs):
    #     if User.objects.filter(username=attrs['username']).exists():
    #         raise serializers.ValidationError('User already exists with this username')
    #     return super().validate(attrs)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)