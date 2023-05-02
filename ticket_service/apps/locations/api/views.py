from rest_framework import permissions, generics
from users.permissions import IsAdminTypeUser,IsManagerTypeUser
from locations.models import Location
from .serializers import LocationSerializer

class LocationListCreateView(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_fields=["is_active","name"]

    def perform_create(self, serializer):
        if self.request.user.is_admin or self.request.user.is_manager :
            serializer.save()
        raise permissions.PermissionDenied


class LocationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAdminTypeUser, IsManagerTypeUser]

    def perform_destroy(self, instance):
        instance.destroy()

