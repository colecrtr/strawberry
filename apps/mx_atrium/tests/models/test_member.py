import datetime
from unittest.mock import patch

import atrium
import faker
from django.test import TestCase
from django.utils import timezone

from apps.mx_atrium.factories import InstitutionFactory
from apps.mx_atrium.factories import MemberFactory
from apps.mx_atrium.factories import UserFactory
from apps.mx_atrium.models import Member


MODULE_UNDER_TEST = "apps.mx_atrium.models.member"
fake = faker.Faker()


class MemberManagerTest(TestCase):
    @patch(f"{MODULE_UNDER_TEST}.mx_atrium_api.get_members", autospec=True)
    def test_update_or_create_from_mx_atrium_update(self, mock_get_members):
        expected_to_update = MemberFactory()
        updated_aggregated_at_datetime = timezone.now()
        mock_get_members.return_value = [
            atrium.Member(
                guid=expected_to_update.guid,
                institution_code=expected_to_update.institution.code,
                user_guid=expected_to_update.user.guid,
                aggregated_at=str(updated_aggregated_at_datetime),
                connection_status=expected_to_update.connection_status.name,
                name=expected_to_update.name,
                successfully_aggregated_at=str(updated_aggregated_at_datetime),
            )
        ]

        Member.objects.update_or_create_from_mx_atrium()

        expected_to_update.refresh_from_db()
        self.assertEqual(
            expected_to_update.aggregated_at, updated_aggregated_at_datetime
        )
        self.assertEqual(
            expected_to_update.successfully_aggregated_at,
            updated_aggregated_at_datetime,
        )

    @patch(f"{MODULE_UNDER_TEST}.mx_atrium_api.get_members", autospec=True)
    def test_update_or_create_from_mx_atrium_create(self, mock_get_members):
        user = UserFactory()
        institution = InstitutionFactory()
        expected_guid = fake.sha1()
        mock_get_members.return_value = [
            atrium.Member(
                guid=expected_guid,
                institution_code=institution.code,
                user_guid=user.guid,
                aggregated_at=str(fake.past_datetime(tzinfo=datetime.timezone.utc)),
                connection_status=fake.random_element(
                    elements=list(Member.ConnectionStatus)
                ).name,
                name=fake.word(),
                successfully_aggregated_at=str(
                    fake.past_datetime(tzinfo=datetime.timezone.utc)
                ),
            )
        ]

        self.assertFalse(Member.objects.filter(guid=expected_guid).exists())
        Member.objects.update_or_create_from_mx_atrium()

        self.assertTrue(Member.objects.filter(guid=expected_guid).exists())
