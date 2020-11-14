from unittest.mock import patch

import atrium
import faker
from django.test import TestCase

from apps.account.factories import UserFactory as AccountUserFactory
from apps.mx_atrium.factories import UserFactory
from apps.mx_atrium.models import User


fake = faker.Faker()


class UserManagerTest(TestCase):
    def test_get_or_create_from_account_user_get(self):
        mx_atrium_user = UserFactory()
        self.assertEqual(
            mx_atrium_user,
            User.objects.get_or_create_from_account_user(
                account_user=mx_atrium_user.account_user
            ),
            msg="Expected to return the existing MX Atrium User for the given Account User",
        )

    @patch("apps.mx_atrium.models.mx_atrium_api", autospec=True)
    def test_get_or_create_from_account_user_create(self, mock_mx_atrium_api):
        new_user = atrium.User(guid=fake.sha1(), is_disabled=fake.pybool())
        mock_mx_atrium_api.users.create_user.return_value.user = new_user

        user = User.objects.get_or_create_from_account_user(
            account_user=AccountUserFactory()
        )

        mock_mx_atrium_api.users.create_user.assert_called()
        self.assertEqual(user.guid, new_user.guid)
        self.assertEqual(user.is_disabled, new_user.is_disabled)


class UserTest(TestCase):
    @patch("apps.mx_atrium.models.mx_atrium_api")
    def test_get_connect_widget_url(self, mock_mx_atrium_api):
        user = UserFactory()
        connect_widget = atrium.ConnectWidget(
            connect_widget_url=fake.url(), guid=user.guid
        )
        mock_mx_atrium_api.connect_widget.get_connect_widget.return_value.user = (
            connect_widget
        )

        user.get_connect_widget_url()

        mock_mx_atrium_api.connect_widget.get_connect_widget.assert_called()
