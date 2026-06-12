from django.utils import timezone
from rest_framework.exceptions import ValidationError

from .models import Appointment


class AppointmentService:

    @staticmethod
    def create_appointment(data):
        appointment_date = data.get("appointment_date")

        # Verifica se o campo foi informado
        if appointment_date is None:
            raise ValidationError(
                {"appointment_date": "O campo appointment_date é obrigatório."}
            )

        # Não permite datas passadas
        if appointment_date <= timezone.now():
            raise ValidationError(
                {
                    "appointment_date": (
                        "Não é permitido agendar consultas em datas ou horários passados."
                    )
                }
            )

        # Cria o agendamento
        return Appointment.objects.create(**data)