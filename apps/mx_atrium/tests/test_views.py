from unittest.mock import patch

import faker
from django.test import TestCase
from django.urls import reverse

from apps.account.factories import UserFactory as AccountUserFactory


fake = faker.Faker()


class ConnectWidgetViewTest(TestCase):
    @patch("apps.mx_atrium.views.User")
    def test_get(self, mock_User):
        account_user = AccountUserFactory()
        expected_url = fake.url()
        method = mock_User.objects.get_or_create_from_account_user
        method = method.return_value.get_connect_widget_url
        method.return_value = expected_url

        self.client.force_login(account_user)
        response = self.client.get(reverse("mx_atrium:connect-widget"))

        method.assert_called()
        self.assertContains(response, f'url: "{expected_url}"')
