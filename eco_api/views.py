from rest_framework import viewsets, permissions
from eco_api.models import Trip, TransportType, EnergySource, User
from eco_api.serializers import TripSerializer, TransportTypeSerializer, EnergySourceSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class IsEditorUser(permissions.BasePermission):
    def has_permission(self, request, view):
         return request.user and request.user.role == 'editor'


class TransportTypeViewSet(viewsets.ModelViewSet):
    queryset = TransportType.objects.all()
    serializer_class = TransportTypeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class EnergySourceViewSet(viewsets.ModelViewSet):
    queryset = EnergySource.objects.all()
    serializer_class = EnergySourceSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.AllowAny]
        elif self.action == 'create':
            permission_classes = [IsAdminUser]
        elif self.action == 'update' or self.action == 'destroy':
             permission_classes = [IsEditorUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]