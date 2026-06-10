from django.shortcuts import render

from appointments.models import Appointment
from professionals.models import Professional


def home(request):
    context = {
        "professionals": Professional.objects.order_by("social_name", "id"),
        "appointments": Appointment.objects.select_related("professional").order_by("-appointment_date", "-id")[:8],
    }
    return render(request, "professionals/cadastro.html", context)