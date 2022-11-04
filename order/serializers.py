from rest_framework import serializers

from core.models import Order, Snack
from core.serializers import SnackSerializer
from child.serializers import ChildSerializer

def calc_order_value(snacks: list) -> float:
    value = 0
    for snack in snacks:
        value += Snack.objects.get(id=snack.id).price
    
    return value


class OrderSerializer(serializers.ModelSerializer):
    childs = ChildSerializer(many=True, read_only=True)
    snacks = SnackSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'order_day', 'date', 'child_id', 'snack_id', 'order_value', 'childs', 'snacks']
        read_only_fields = ['id', 'order_value']
    
    def _set_snack_id(self, snacks, order):
        for snack in snacks:
            order.snack_id.add(snack)
    
    def create(self, validated_data):
        snacks = validated_data.pop('snack_id', [])
        
        order = Order.objects.create(**validated_data)
        order.order_value = calc_order_value(snacks)
        order.save()
        self._set_snack_id(snacks=snacks, order=order)

        return order
    
    def update(self, instance, validated_data):
        snacks = validated_data.pop('snack_id', None)
        if snacks is not None:
            instance.snack_id.clear()
            self._set_snack_id(snacks=snacks, order=instance)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance
        