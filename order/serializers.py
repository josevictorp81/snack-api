from rest_framework import serializers
from datetime import date

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
        fields = ['id', 'date', 'child_id', 'snack_id', 'order_value', 'created_at']
        read_only_fields = ['id', 'order_value', 'created_at']
    
    def _set_snack_id(self, snacks, order) -> None:
        """ set snacks id on order """
        for snack in snacks:
            order.snack_id.add(snack)
    
    def _verify_father(self, child_id: int) -> bool:
        """ verifying if the logged user is the parent of the child passed as a parameter """
        child = Child.objects.get(id=child_id)

        if child.father == self.context['request'].user:
            return True
        return False
    
    def _verify_has_order(self, child_id: int, date) -> bool:
        """ verifying if has order for the parameter day """
        order = Order.objects.filter(child_id=child_id, date=date)
        if order.exists():
            return True
        return False
    
    def _verify_prev_date(self, date_order):
        """ verifying if the date is prev then currenty day """
        return date_order < date.today()
    
    def validate(self, attrs):
        """ validating input data """
        date_order = attrs['date']
        child_id = attrs['child_id']

        if not self._verify_father(child_id=child_id.id):
            msg = {'detail': 'This child are not your son!'}
            raise serializers.ValidationError(detail=msg)

        if self._verify_prev_date(date_order=date_order):
            msg = {'detail': 'It is not possible to place an order for a day before the current day!'}
            raise serializers.ValidationError(detail=msg)

        if self._verify_has_order(child_id=child_id.id, date=date_order):
            msg = {'detail': 'You already ordered for that day!'}
            raise serializers.ValidationError(detail=msg) 

        return super().validate(attrs)



    def create(self, validated_data):
        """ create order """
        snacks = validated_data.pop('snack_id', [])
        
        order = Order.objects.create(**validated_data)
        order.order_value = calc_order_value(snacks)
        order.save()
        self._set_snack_id(snacks=snacks, order=order)

        return order        
    
    def update(self, instance, validated_data):
        """ update existing order """
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
        fields = ['id', 'date', 'child_id', 'snack_id', 'order_value', 'created_at']
        read_only_fields = fields
        