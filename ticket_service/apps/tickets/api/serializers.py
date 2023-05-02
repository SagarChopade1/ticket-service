from rest_framework import serializers
from tickets.models import Ticket
from tickets.utils import DistancePriceCalculator, calculate_distance

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('id', 'created_by', 'transportation_type', 'passenger',"passenger_name", 'source', 'destination', 'seat_number', 'price', 'currency_type', 'journey_start_time', 'journey_end_time',  'is_qr_code_valid', 'is_cancelled')
        read_only_fields = ('id', "created_by")

    def validate(self, data):
        if data['source'] == data['destination']:
            raise serializers.ValidationError("Source and destination cannot be the same.")
        
        distance_in_meter=calculate_distance.get_distance(data['source'], data['destination'])
        if not distance_in_meter:
            raise serializers.ValidationError("Distance calculation service is not available for now please try again later")
        expected_price=float(round(DistancePriceCalculator.get_price(distance_in_meter, data['transportation_type'].type,data["currency_type"]),2))
        if float(data['price'])!=expected_price:
            raise serializers.ValidationError(f"Ticket price should be {expected_price}")
        return data


class TicketSummarySerializer(serializers.Serializer):
    location_name = serializers.CharField()
    year= serializers.CharField()
    month= serializers.CharField()
    count = serializers.IntegerField()


class TicketCostSummarySerializer(serializers.Serializer):
    month = serializers.CharField()
    year = serializers.IntegerField()
    location_name = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)


class TicketUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('is_cancelled',)