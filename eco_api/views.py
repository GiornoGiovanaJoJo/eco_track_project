from rest_framework import viewsets, permissions
from .permissions import IsAdminUser, IsEditorUser, IsAuthenticatedOrReadonly
from .models import Trip
from .serializers import TripSerializer
from rest_framework.response import Response
from rest_framework import status


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAdminUser]
        elif self.action == 'update' or self.action == 'destroy':
            permission_classes = [IsEditorUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = TripSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer