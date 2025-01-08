from rest_framework import serializers
from eco_api.models import Trip, TransportType, EnergySource, User


class TransportTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportType
        fields = ['id', 'name']

class EnergySourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnergySource
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']

class TripSerializer(serializers.ModelSerializer):
    transport_type = TransportTypeSerializer(read_only=True)
    energy_source = EnergySourceSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Trip
        fields = ['id', 'user', 'start_date', 'end_date', 'transport_type', 'energy_source', 'distance', 'passengers', 'co2_emissions', 'other_emissions']