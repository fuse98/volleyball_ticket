from rest_framework import serializers
from matches.models import Stadium, SeatingArrangment, Seat


class StadiumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stadium
        fields = ['id', 'title', 'address', 'lat', 'long']

    def validate_lat(self, value):
        if not (-90 <= value <= 90):
            raise serializers.ValidationError("Latitude must be between -90 and 90.")
        return value

    def validate_long(self, value):
        if not (-180 <= value <= 180):
            raise serializers.ValidationError("Longitude must be between -180 and 180.")
        return value


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'column', 'row', 'section', 'pos_x', 'pos_y']


class SeatingArrangementSerializer(serializers.ModelSerializer):
    seats = SeatSerializer(many=True)

    class Meta:
        model = SeatingArrangment
        fields = ['id', 'stadium', 'seats']

    def create(self, validated_data):
        seats_data = validated_data.pop('seats')
        seating_arrangement = SeatingArrangment.objects.create(**validated_data)

        seats = []
        for seat_data in seats_data:
            seats.append(Seat(seating_arrangment=seating_arrangement, **seat_data))
        Seat.objects.bulk_create(seats, batch_size=1000)

        return seating_arrangement
