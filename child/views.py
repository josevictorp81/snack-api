from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import ChildSerializer, ReadChildSerializer
from core.models import Child

class ChildListAPIView(ListAPIView):
    serializer_class = ReadChildSerializer
    queryset = Child.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(father=self.request.user)


class ChildCreateAPIView(CreateAPIView):
    serializer_class = ChildSerializer
    queryset = Child.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        serializer.save(father=self.request.user)
        