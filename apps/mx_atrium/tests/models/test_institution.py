from unittest.mock import patch

import atrium
import faker
from django.test import TestCase

from apps.mx_atrium.factories import InstitutionFactory
from apps.mx_atrium.models import Institution


MODULE_UNDER_TEST = "apps.mx_atrium.models.institution"
fake = faker.Faker()


class InstitutionManagerTest(TestCase):
    @patch(f"{MODULE_UNDER_TEST}.mx_atrium_api.get_institution", autospec=True)
    def test_get_or_create_from_mx_atrium_get(self, mock_get_institution):
        expected = InstitutionFactory()

        actual, created = Institution.objects.get_or_create_from_mx_atrium(
            code=expected.code
        )

        self.assertEqual(expected.pk, actual.pk)
        self.assertFalse(created)
        mock_get_institution.assert_not_called()

    @patch(f"{MODULE_UNDER_TEST}.mx_atrium_api.get_institution", autospec=True)
    def test_get_or_create_from_mx_atrium_create(self, mock_get_institution):
        expected_code = fake.word()
        mock_get_institution.return_value = atrium.Institution(
            code=expected_code,
            name=fake.word(),
            small_logo_url=fake.url(),
            medium_logo_url=fake.url(),
            url=fake.url(),
        )

        institution, created = Institution.objects.get_or_create_from_mx_atrium(
            code=expected_code
        )

        self.assertTrue(created)
        mock_get_institution.assert_called_with(code=expected_code)
