from django.test import TestCase
from django.urls import reverse


class RootRedirectTestCase(TestCase):
    def test_root_renders_registration_page(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Entrar com JWT")
        self.assertContains(response, "Cadastro de profissional")
        self.assertContains(response, "Cadastro de consulta")
