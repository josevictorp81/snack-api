from rest_framework import serializers

from .utils import generate_code
from core.models import Child
from user.serializers import UserSerializer
from core.serializers import ClassesSerializer

class ChildSerializer(serializers.ModelSerializer):
    father = UserSerializer(read_only=True)
    classes = ClassesSerializer(read_only=True)

    class Meta:
        model = Child
        fields = ['id', 'name', 'code', 'class_id', 'father', 'classes']
        read_only_fields = ['id', 'code']
    
    def create(self, validated_data):
        code = generate_code()

        child = Child.objects.create(**validated_data)
        child.code = code
        child.save()

        return child
