from rest_framework import serializers
from .models import Trip

class TripSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True) # <- Добавляем это
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    transport_type = serializers.CharField(max_length=100)
    distance = serializers.FloatField()
    passengers = serializers.IntegerField()
    energy_source = serializers.CharField(max_length=100)
    co2_emissions = serializers.FloatField(required=False)
    other_emissions = serializers.JSONField(required=False, allow_null=True, default=dict)

    class Meta:
        model = Trip
        fields = '__all__'