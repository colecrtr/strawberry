from django.conf import settings
from django.test import TestCase


class SettingsTest(TestCase):
    def test_not_running_in_production(self):
        self.assertEqual(settings.ENVIRONMENT, "local", msg="Only run tests locally")
