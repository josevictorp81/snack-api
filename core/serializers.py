from rest_framework import serializers

from core.models import Classes

class ClassesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classes
        fields = ['id', 'name']
        read_only_fields = fields
        