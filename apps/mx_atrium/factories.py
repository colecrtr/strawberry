import datetime

import factory

from apps.account.factories import UserFactory as AccountUserFactory

from .models import Member


class InstitutionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "mx_atrium.Institution"

    code = factory.Faker("word")
    name = factory.Faker("name")


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "mx_atrium.User"

    account_user = factory.SubFactory(AccountUserFactory)
    guid = factory.Faker("sha1")
    is_disabled = factory.Faker("pybool")


class MemberFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "mx_atrium.Member"

    institution = factory.SubFactory(InstitutionFactory)
    user = factory.SubFactory(UserFactory)
    aggregated_at = factory.Faker("past_datetime", tzinfo=datetime.timezone.utc)
    connection_status = factory.Faker(
        "random_element", elements=list(Member.ConnectionStatus)
    )
    guid = factory.Faker("sha1")
    name = factory.Faker("word")
    successfully_aggregated_at = factory.Faker(
        "past_datetime", tzinfo=datetime.timezone.utc
    )
