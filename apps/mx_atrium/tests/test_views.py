from unittest.mock import MagicMock
from unittest.mock import patch

import faker
from django.test import TestCase
from django.urls import reverse

from apps.account.factories import UserFactory as AccountUserFactory


fake = faker.Faker()


class ConnectWidgetViewTest(TestCase):
    @patch("apps.mx_atrium.views.User.objects.get_or_create_from_mx_atrium")
    def test_get(self, mock_get_or_create_from_mx_atrium):
        account_user = AccountUserFactory()
        expected_url = fake.url()
        mock_get_or_create_from_mx_atrium.return_value = (
            MagicMock(**{"get_connect_widget_url.return_value": expected_url}),
            fake.pybool(),
        )

        self.client.force_login(account_user)
        response = self.client.get(reverse("mx_atrium:connect-widget"))

        self.assertContains(response, f'url: "{expected_url}"')
