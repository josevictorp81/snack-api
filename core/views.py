from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import ClassesSerializer
from core.models import Classes

class ClassesListAPIView(ListAPIView):
    serializer_class = ClassesSerializer
    queryset = Classes.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    