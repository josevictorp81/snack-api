from rest_framework import serializers

from core.models import Classes, Snack

class ClassesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classes
        fields = ['id', 'name']
        read_only_fields = fields


class SnackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snack
        fields = ['name', 'price', 'available']
        read_only_fields = fields
        