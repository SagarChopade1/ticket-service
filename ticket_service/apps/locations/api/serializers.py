from rest_framework import serializers
from rest_framework import serializers
from locations.models import Location

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
        read_only_fields = ["created_at","updated_at"]
