from unittest.mock import patch

import atrium
import faker
from django.test import TestCase

from apps.account.factories import UserFactory as AccountUserFactory
from apps.mx_atrium.factories import UserFactory
from apps.mx_atrium.models import User


MODULE_UNDER_TEST = "apps.mx_atrium.models.user"
fake = faker.Faker()


class UserManagerTest(TestCase):
    @patch(f"{MODULE_UNDER_TEST}.mx_atrium_api.get_users", autospec=True)
    def test_update_from_mx_atrium_update(self, mock_get_users):
        user_to_update = UserFactory(is_disabled=False)
        mock_get_users.return_value = [
            atrium.User(
                guid=user_to_update.guid, identifier=user_to_update.pk, is_disabled=True
            )
        ]

        self.assertFalse(user_to_update.is_disabled)
        User.objects.update_from_mx_atrium()

        user_to_update.refresh_from_db()
        self.assertTrue(user_to_update.is_disabled)

    @patch(f"{MODULE_UNDER_TEST}.logger.error", autospec=True)
    @patch(f"{MODULE_UNDER_TEST}.mx_atrium_api.get_users", autospec=True)
    def test_update_from_mx_atrium_create(self, mock_get_users, mock_error):
        mock_get_users.return_value = [
            atrium.User(guid=fake.sha1(), identifier=str(100), is_disabled=True)
        ]

        self.assertEqual(User.objects.all().count(), 0)
        User.objects.update_from_mx_atrium()

        self.assertEqual(User.objects.all().count(), 0)
        mock_error.assert_called()

    def test_get_or_create_from_mx_atrium_get(self):
        expected = UserFactory()

        actual, _created = User.objects.get_or_create_from_mx_atrium(
            account_user=expected.account_user
        )

        self.assertEqual(
            expected,
            actual,
            msg="Expected to return the existing MX Atrium User for the given Account User",
        )

    @patch("apps.mx_atrium.models.user.mx_atrium_api.create_user", autospec=True)
    def test_get_or_create_from_mx_atrium_create(self, mock_create_user):
        user_data = atrium.User(guid=fake.sha1(), is_disabled=fake.pybool())
        mock_create_user.return_value = user_data

        user, _created = User.objects.get_or_create_from_mx_atrium(
            account_user=AccountUserFactory()
        )

        mock_create_user.assert_called()
        self.assertEqual(user.guid, user_data.guid)
        self.assertEqual(user.is_disabled, user_data.is_disabled)


class UserTest(TestCase):
    @patch("apps.mx_atrium.models.user.mx_atrium_api.get_connect_widget_url")
    def test_get_connect_widget_url(self, mock_get_connect_widget_url):
        user = UserFactory()
        mock_get_connect_widget_url.return_value = fake.url()

        user.get_connect_widget_url()

        mock_get_connect_widget_url.assert_called()
