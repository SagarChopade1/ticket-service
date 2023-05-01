from rest_framework import permissions, status, response, generics
from rest_framework.views import APIView
from users.api.serializers import UserRegistrationSerializer, UserUpdateSerializer
from users.models import User


class RegistrationView(APIView):
    """
    Use this endpoint to register new user.
    """

    serializer_class = UserRegistrationSerializer

    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    """Use this endpoint to retrieve/update user."""

    model = User
    serializer_class = UserRegistrationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(instance=request.user)
        return response.Response(data=serializer.data)

    def patch(self, request):
        serializer = UserUpdateSerializer(instance=request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(data=serializer.data)
