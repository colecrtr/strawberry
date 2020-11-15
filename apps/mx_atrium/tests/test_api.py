from unittest.mock import MagicMock
from unittest.mock import patch

import atrium
import faker
from django.test import TestCase

from apps.mx_atrium.api import MXAtriumAPI
from apps.mx_atrium.api import mx_atrium_api
from apps.mx_atrium.factories import UserFactory


MODULE_UNDER_TEST = "apps.mx_atrium.api"
fake = faker.Faker()


class MXAtriumAPITest(TestCase):
    def test_get_objects_generator(self):
        list_method = MagicMock(
            return_value=MagicMock(
                data_key=[atrium.User()],
                pagination=MagicMock(total_pages=1),
            )
        )
        objects = list(
            MXAtriumAPI.get_objects_generator(
                list_method=list_method,
                list_method_kwargs={},
                data_key="data_key",
                obj_type=atrium.User,
            )
        )

        list_method.assert_called_once()
        self.assertEqual(len(objects), 1)
        self.assertIsInstance(objects[0], atrium.User)

    @patch(f"{MODULE_UNDER_TEST}.mx_atrium_api.connect_widget.get_connect_widget")
    def test_get_connect_widget_url(self, mock_get_connect_widget):
        expected_url = fake.url()
        user = UserFactory()
        mock_get_connect_widget.return_value.user = atrium.ConnectWidget(
            connect_widget_url=expected_url, guid=user.guid
        )

        actual_url = mx_atrium_api.get_connect_widget_url(user_guid=user.guid)

        mock_get_connect_widget.assert_called()
        self.assertEqual(expected_url, actual_url)

    @patch(f"{MODULE_UNDER_TEST}.mx_atrium_api.institutions.read_institution")
    def test_get_institutions(self, mock_read_institution):
        expected = atrium.Institution()
        mock_read_institution.return_value.institution = expected

        actual = mx_atrium_api.get_institution(code=fake.name())

        self.assertIs(actual, expected)

    @patch(f"{MODULE_UNDER_TEST}.mx_atrium_api.users.create_user")
    def test_create_user(self, mock_create_user):
        expected = atrium.User()
        mock_create_user.return_value.user = expected

        actual = mx_atrium_api.create_user(
            identifier=fake.sha1(), is_disabled=fake.pybool()
        )

        self.assertIs(actual, expected)

    @patch(f"{MODULE_UNDER_TEST}.mx_atrium_api.users.list_users")
    def test_get_users(self, mock_list_users):
        expected = atrium.User()
        mock_list_users.return_value = MagicMock(
            users=[expected],
            pagination=MagicMock(total_pages=1),
        )

        actual = list(mx_atrium_api.get_users())

        self.assertEqual(len(actual), 1)
        self.assertIs(actual[0], expected)

    @patch(f"{MODULE_UNDER_TEST}.mx_atrium_api.members.list_members")
    def test_get_members(self, mock_list_members):
        expected = atrium.Member()
        mock_list_members.return_value = MagicMock(
            members=[expected], pagination=MagicMock(total_pages=2)
        )

        actual = list(mx_atrium_api.get_members())

        self.assertEqual(len(actual), 2)
        self.assertIs(actual[0], expected)
        self.assertIs(actual[1], expected)
