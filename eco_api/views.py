from .serializers import TripSerializer
from .models import Trip
from rest_framework import viewsets, permissions
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .permissions import IsAdminUser, IsEditorUser, IsAuthenticatedOrReadonly


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [permissions.IsAuthenticated] # <-- Установили IsAuthenticated

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.AllowAny]
        elif self.action == 'create':
            permission_classes = [IsAdminUser]  # <--- Здесь используем кастомный пермишен
        elif self.action == 'update' or self.action == 'destroy':
            permission_classes = [IsEditorUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = TripSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
def obtain_token_pair(request):
    if request.method == 'POST':
      token = obtain_auth_token(request)
      return Response(token.data)