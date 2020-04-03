from django.test import TestCase
from django.test.client import Client
from django.urls import reverse


class HomeViewTest(TestCase):
    def test_home_status_code(self):
        client = Client()
        response = client.get(reverse('core_home'))
        self.assertEqual(response.status_code, 200)
