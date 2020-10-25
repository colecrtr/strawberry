from django.conf import settings
from django.test import TestCase


class SettingsTest(TestCase):
    def test_not_running_in_production(self):
        self.assertFalse(settings.IS_PRODUCTION, msg="Don't run tests in production.")
