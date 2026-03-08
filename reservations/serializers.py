from rest_framework import serializers
from .models import Reservation 
from django.core.exceptions import ValidationError
from .services import reservation_service 

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation  
        fields = "__all__"
        read_only_fields = ("id", "user", "created_at", "qr_token", "status")

    # Validaciones API 
    def validate(self, attrs):
        #solo validaciones request
        return attrs 

    #Crear reserva
    def create(self, validated_data): 
        request = self.context["request"]
        user = request.user

        service = reservation_service.ReservationService() 
        return service.create_reservation(
            user = user,
            **validated_data
        )
        
    #Actualizar reserva
    def update(self, instance, validated_data):
        service = reservation_service.ReservationService()
        return service.update_reservation(instance, validated_data)

class ReservationCalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ("space", "status", "start_date", "end_date")
        read_only_fields = fields 


        