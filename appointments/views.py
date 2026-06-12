from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from appointments.models import Appointment
from appointments.serializers import AppointmentSerializer
from appointments.services import AppointmentService


class PlainTextJSONParser(JSONParser):
    media_type = "text/plain"


class AppointmentViewSet(ModelViewSet):
    queryset = Appointment.objects.select_related("professional").all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [PlainTextJSONParser, JSONParser]

    @action(detail=False, methods=["get"], url_path="professional/(?P<professional_id>[^/.]+)")
    def by_professional(self, request, professional_id=None):
        appointments = self.get_queryset().filter(professional_id=professional_id)
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)
    
class AppointmentViewSet(ModelViewSet):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()

    def perform_create(self, serializer):
        AppointmentService.create_appointment(
            serializer.validated_data
        )