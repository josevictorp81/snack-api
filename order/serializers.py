from rest_framework import serializers

from core.models import Order, Snack, Child
from core.serializers import SnackSerializer
from child.serializers import ReadChildSerializer

def calc_order_value(snacks: list) -> float:
    value = 0
    for snack in snacks:
        value += Snack.objects.get(id=snack.id).price
    
    return value


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'date', 'child_id', 'snack_id', 'order_value']
        read_only_fields = ['id', 'order_value']
    
    def _set_snack_id(self, snacks, order) -> None:
        for snack in snacks:
            order.snack_id.add(snack)
    
    def _verify_father(self, child_id: int) -> bool:
        child = Child.objects.get(id=child_id)

        if child.father == self.context['request'].user:
            return True
        return False
    
    def _verify_has_order(self, child_id: int, date) -> bool:
        order = Order.objects.filter(child_id=child_id, date=date)
        if order.exists():
            return True
        return False

    def create(self, validated_data):
        snacks = validated_data.pop('snack_id', [])
        child_id = validated_data['child_id']
        date = validated_data['date']

        father = self._verify_father(child_id=child_id.id)

        has_order = self._verify_has_order(child_id=child_id.id, date=date)
        
        if father:
            if not has_order:
                order = Order.objects.create(**validated_data)
                order.order_value = calc_order_value(snacks)
                order.save()
                self._set_snack_id(snacks=snacks, order=order)

                return order
            else:
                msg = {
                'detail': 'You already ordered for that day!'
            }
            raise serializers.ValidationError(detail=msg)    
        else:
            msg = {
                'detail': 'This child are not your son!'
            }
            raise serializers.ValidationError(detail=msg)         
    
    def update(self, instance, validated_data):
        snacks = validated_data.pop('snack_id', None)
        if snacks is not None:
            instance.snack_id.clear()
            self._set_snack_id(snacks=snacks, order=instance)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance


class ReadOrderSerializer(serializers.ModelSerializer):
    child_id = ReadChildSerializer()
    snack_id = SnackSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'date', 'child_id', 'snack_id', 'order_value']
        read_only_fields = fields
        