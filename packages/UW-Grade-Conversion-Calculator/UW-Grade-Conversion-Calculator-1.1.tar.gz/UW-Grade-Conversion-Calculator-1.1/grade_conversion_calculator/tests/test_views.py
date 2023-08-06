from django.test import TestCase
from django.urls import reverse


class ViewTest(TestCase):
    def test_demo(self):
        response = self.client.get(reverse('calculator_demo'))
        self.assertEqual(response.status_code, 200)

    def test_javascript_catalog(self):
        response = self.client.get(reverse('javascript-catalog'))
        self.assertEqual(response.status_code, 200)
