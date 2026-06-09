from datetime import timedelta

from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from appointments.models import Appointment
from professionals.models import Professional


class AppointmentAPITestCase(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user(username="tester", password="strong-password-123")
		token = RefreshToken.for_user(self.user)
		self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")
		self.professional = Professional.objects.create(
			social_name="Dra. Ana",
			profession="Psicóloga",
			address="Rua A, 100",
			contact="ana@example.com",
		)
		self.list_url = reverse("appointment-list")

	def test_create_appointment(self):
		appointment_date = timezone.now() + timedelta(days=1)
		payload = {
			"professional": self.professional.id,
			"appointment_date": appointment_date.isoformat(),
		}
		response = self.client.post(self.list_url, payload, format="json")
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(Appointment.objects.count(), 1)

	def test_list_appointments(self):
		appointment_date = timezone.now() + timedelta(days=1)
		Appointment.objects.create(
			professional=self.professional,
			appointment_date=appointment_date,
		)
		response = self.client.get(self.list_url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data), 1)

	def test_update_appointment(self):
		appointment_date = timezone.now() + timedelta(days=1)
		appointment = Appointment.objects.create(
			professional=self.professional,
			appointment_date=appointment_date,
		)
		detail_url = reverse("appointment-detail", args=[appointment.id])
		updated_date = timezone.now() + timedelta(days=2)
		response = self.client.patch(
			detail_url,
			{"appointment_date": updated_date.isoformat()},
			format="json",
		)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		appointment.refresh_from_db()
		self.assertEqual(
			appointment.appointment_date.replace(microsecond=0),
			updated_date.replace(microsecond=0),
		)

	def test_delete_appointment(self):
		appointment_date = timezone.now() + timedelta(days=1)
		appointment = Appointment.objects.create(
			professional=self.professional,
			appointment_date=appointment_date,
		)
		detail_url = reverse("appointment-detail", args=[appointment.id])
		response = self.client.delete(detail_url)
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
		self.assertEqual(Appointment.objects.count(), 0)

	def test_find_appointments_by_professional(self):
		appointment_date = timezone.now() + timedelta(days=1)
		Appointment.objects.create(
			professional=self.professional,
			appointment_date=appointment_date,
		)
		response = self.client.get(reverse("appointment-by-professional", args=[self.professional.id]))
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data), 1)

	def test_invalid_appointment_payload(self):
		response = self.client.post(self.list_url, {}, format="json")
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
