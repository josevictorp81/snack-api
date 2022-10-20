from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import ClassesSerializer, SnackSerializer
from core.models import Classes, Snack

class ClassesListAPIView(ListAPIView):
    serializer_class = ClassesSerializer
    queryset = Classes.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


class SnackListAPIView(ListAPIView):
    serializer_class = SnackSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = Snack.objects.all()
    