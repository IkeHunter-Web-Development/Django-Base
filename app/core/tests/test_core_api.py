"""
General and core api tests.
"""

from django.urls import reverse
from rest_framework import status
from core.abstracts.tests import ApiTestsBase


class CoreApiTests(ApiTestsBase):

    def test_api_docs(self):
        """Docs should give 200 status."""
        res = self.client.get(reverse("api-docs"))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_api_schema(self):
        """Schema should give 200 status."""
        res = self.client.get(reverse("api-schema"))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
