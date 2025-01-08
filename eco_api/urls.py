from django.urls import path, include
from rest_framework import routers
from eco_api import views

router = routers.DefaultRouter()
router.register(r'trips', views.TripViewSet, basename='trip')
router.register(r'transport_types', views.TransportTypeViewSet, basename='transport_type')
router.register(r'energy_sources', views.EnergySourceViewSet, basename='energy_source')
router.register(r'users', views.UserViewSet, basename='user')


urlpatterns = [
    path('', include(router.urls)),
]