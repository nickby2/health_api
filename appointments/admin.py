from django.contrib import admin

from appointments.models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
	list_display = ("id", "professional", "appointment_date", "created_at")
	search_fields = ("professional__social_name",)
