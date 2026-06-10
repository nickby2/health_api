from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from professionals.models import Professional


class ProfessionalAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="strong-password-123")
        token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")
        self.list_url = reverse("professional-list")

    def test_create_professional(self):
        payload = {
            "social_name": "Dra. Ana",
            "profession": "Psicóloga",
            "address": "Rua A, 100",
            "contact": "ana@example.com",
        }
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Professional.objects.count(), 1)

    def test_list_professionals(self):
        Professional.objects.create(
            social_name="Dra. Ana",
            profession="Psicóloga",
            address="Rua A, 100",
            contact="ana@example.com",
        )
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_professional(self):
        professional = Professional.objects.create(
            social_name="Dra. Ana",
            profession="Psicóloga",
            address="Rua A, 100",
            contact="ana@example.com",
        )
        detail_url = reverse("professional-detail", args=[professional.id])
        response = self.client.patch(detail_url, {"contact": "ana@lacrei.org"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        professional.refresh_from_db()
        self.assertEqual(professional.contact, "ana@lacrei.org")

    def test_delete_professional(self):
        professional = Professional.objects.create(
            social_name="Dra. Ana",
            profession="Psicóloga",
            address="Rua A, 100",
            contact="ana@example.com",
        )
        detail_url = reverse("professional-detail", args=[professional.id])
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Professional.objects.count(), 0)

    def test_invalid_professional_payload(self):
        response = self.client.post(self.list_url, {"social_name": "A"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
