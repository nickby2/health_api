from django.utils import timezone
from rest_framework import serializers
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):

    def validate_scheduled_at(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError(
                "Não é permitido agendar consultas em datas ou horários passados."
            )
        return value

    class Meta:
        model = Appointment
        fields = "__all__"