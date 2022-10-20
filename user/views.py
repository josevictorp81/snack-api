from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer

class UserCreateAPIView(CreateAPIView):
    """ create user """
    serializer_class = UserSerializer


class UserManagerAPIView(RetrieveAPIView):
    """ manager user profile """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        """ get user authenticated """
        return self.request.user