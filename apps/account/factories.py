import factory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "account.User"

    is_active = True

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.LazyAttribute(
        lambda o: f"{o.first_name.lower()}_{o.last_name.lower()}"
    )
    email = factory.LazyAttribute(
        lambda o: f"{o.first_name.lower()}.{o.last_name.lower()}@example.org"
    )
