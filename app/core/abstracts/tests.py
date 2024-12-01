import os
from django import forms
from django.test import TestCase
from django.urls import reverse
from rest_framework import serializers
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APIClient

from users.tests.utils import create_test_superuser


class TestsBase(TestCase):
    """Abstract testing utilities."""

    def assertObjHasFields(self, object, fields: dict):
        """Object fields should match given field values."""
        for key, value in fields.items():
            obj_value = getattr(object, key)
            self.assertEqual(obj_value, value)

    def assertNotImplemented(self):
        """Mark a test as not implemented, should fail."""
        self.fail("Method is not implemented.")

    def assertLength(self, target: list, length=1, msg=None):
        """Provided list should be specified length."""
        if msg is None:
            msg = f"Invalid length of {len(target)}, expected {length}."

        self.assertEqual(len(target), length, msg)

    def assertStartsWith(self, string: str, substring: str):
        """Target string should start with substring."""

        self.assertIsInstance(string, str)
        self.assertTrue(
            string.startswith(substring),
            f"String {string} does not start with {substring}.",
        )

    def assertEndsWith(self, string: str, substring: str):
        """Target string should end with substring."""

        self.assertIsInstance(string, str)
        self.assertTrue(
            string.endswith(substring),
            f"String {string} does not end with {substring}.",
        )

    def assertFileExists(self, path):
        """File with path should exist."""

        self.assertTrue(os.path.exists(path), f"File does not exist at {path}.")

    def assertValidSerializer(self, serializer: serializers.Serializer):
        """Check `.is_valid()` function on serializer, prints errors if invalid."""

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def assertListIsSubset(self, outer_list: list, inner_list: list):
        """Inner list should be a strict subset of outer list."""

        excluded = [item for item in inner_list if item not in outer_list]

        self.assertEqual(
            len(excluded),
            0,
            f"The outer list does not contain these values: {', '.join(excluded)}.",
        )


class ApiTestsBase(TestsBase):
    """Abstract testing utilities for api testing."""

    def setUp(self):
        self.client = APIClient()


class ViewsTestsBase(ApiTestsBase):
    """Abstract testing utilities for app views."""

    def assertRenders(self, url: str, *args, **kwargs):
        """Reversible url should return 200."""
        path = reverse(url, args=[*args], kwargs={**kwargs})
        res = self.client.get(path)

        self.assertEqual(res.status_code, HTTP_200_OK)


class AuthViewsTestsBase(ViewsTestsBase):
    """Abstract testing utilities for app views that require auth."""

    def setUp(self):
        super().setUp()
        self.user = create_test_superuser()

        self.client = APIClient()
        self.client.force_login(user=self.user)


class FormTestsBase(TestsBase):
    """Testing utility methods for form submissions."""

    form: forms.ModelForm = None

    def assertSubmitForm(self, data, *args, **kwargs):
        """Should be able to submit data (and optinally args, kwargs) to form.
        Returns form.clean()
        """
        form_data = self.form(data=data, *args, **kwargs)
        self.assertFalse(form_data.errors, f"Form returned errors: {form_data.errors}")
        self.assertTrue(form_data.is_valid())

        res_data = form_data.clean()
        self.assertFalse(form_data.errors, f"Cleaned form returned errors: {form_data.errors}")
        return res_data
