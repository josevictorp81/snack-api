from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.models import Order
from .serializers import OrderSerializer, ReadOrderSerializer
from .pagination import CustomPageNumberPagination


class OrderListAPIView(ListAPIView):
    serializer_class = ReadOrderSerializer
    queryset = Order.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        """ list all order of a child filter by authenticated user/father """
        return self.queryset.filter(child_id__father=self.request.user).order_by('-created_at')


class OrderRetrieveAPIView(RetrieveAPIView):
    serializer_class = ReadOrderSerializer
    queryset = Order.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ list all order of a child filter by authenticated user/father """
        return self.queryset.filter(child_id__father=self.request.user)


class OrderCreateAPIView(CreateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class OrderUpdateAPIView(UpdateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ list all order of a child filter by authenticated user/father """
        return self.queryset.filter(child_id__father=self.request.user)


class OrderDeleteAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = Order.objects.all()

    def get_queryset(self):
        """ list all order of a child filter by authenticated user/father """
        return self.queryset.filter(child_id__father=self.request.user)
