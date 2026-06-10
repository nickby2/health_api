from django.db import models


class Appointment(models.Model):
    professional = models.ForeignKey(
        "professionals.Professional",
        on_delete=models.CASCADE,
        related_name="appointments",
    )
    appointment_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-appointment_date", "-id"]

    def __str__(self):
        return f"Consulta #{self.pk}"