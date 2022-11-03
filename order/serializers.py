from rest_framework import serializers

from core.models import Order, Snack, Child
from core.serializers import SnackSerializer
from child.serializers import ChildSerializer

class OrderSerializer(serializers.ModelSerializer):
    childs = ChildSerializer(read_only=True)
    snacks = SnackSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'order_day', 'date', 'child_id', 'snack_id', 'order_value', 'childs', 'snacks']
        read_only_fields = ['id', 'order_value']