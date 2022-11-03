from django.contrib import admin

from .models import Classes, Snack, Child, Order

@admin.register(Classes)
class ClassesAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Snack)
class SnackAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'available']


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'class_id', 'father']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_day', 'date', 'child_id', 'order_value', 'created_at']
