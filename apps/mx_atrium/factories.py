import factory

from apps.account.factories import UserFactory as AccountUserFactory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "mx_atrium.User"

    account_user = factory.SubFactory(AccountUserFactory)
    guid = factory.Faker("sha1")
    is_disabled = factory.Faker("pybool")
