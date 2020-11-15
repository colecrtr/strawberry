import logging

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.account.models import User as AccountUser
from apps.mx_atrium.api import mx_atrium_api
from project.models import BaseModel


logger = logging.getLogger(__name__)


class UserManager(models.Manager):
    def update_from_mx_atrium(self):
        """Updates MX Atrium Users in our database to match theirs"""

        for user_data in mx_atrium_api.get_users():
            try:
                user = self.get(guid=user_data.guid)
                user.is_disabled = user_data.is_disabled
                user.save()
            except self.model.DoesNotExist as e:
                logger.error(
                    f"Cannot update MX Atrium User ({user_data.guid}) that does not exist in this "
                    f"system",
                    e,
                )

    def get_or_create_from_mx_atrium(self, account_user: AccountUser) -> ("User", bool):
        """Gets or creates MX Atrium Users for the given account_user"""

        try:
            user = self.get(account_user=account_user)
            created = False
        except self.model.DoesNotExist:
            user_data = mx_atrium_api.create_user(
                identifier=str(account_user.pk),
                is_disabled=(not account_user.is_active),
            )
            user = self.create(
                account_user=account_user,
                guid=user_data.guid,
                is_disabled=user_data.is_disabled,
            )
            created = True

        logger.info(f"{'Created' if created else 'Updated'} {user}")

        return user, created


class User(BaseModel):
    """MX Atrium User

    Docs: https://atrium.mx.com/docs#users
    """

    objects = UserManager()

    account_user = models.OneToOneField(
        to="account.User",
        on_delete=models.CASCADE,
        verbose_name=_("Account User"),
        help_text=_("Application User this MX Atrium User belongs to"),
    )

    # MX Atrium fields (docs: https://atrium.mx.com/docs#user-fields)
    # - `identifier` is `id`/`pk`
    # - `metadata` is unused
    guid = models.CharField(
        max_length=256,
        unique=True,
        verbose_name=_("MX Atrium guid"),
        help_text=_("A unique identifier, defined by MX."),
    )
    is_disabled = models.BooleanField(
        verbose_name=_("MX Atrium is_disabled"),
        help_text=_("True if you want the user disabled, false otherwise."),
    )

    def __str__(self) -> str:
        return self.guid

    def get_connect_widget_url(self) -> str:
        """Gets the URL used for the MX Atrium Connect Widget config on the frontend

        :return: MX Atrium Connect Widget URL string
        """

        return mx_atrium_api.get_connect_widget_url(user_guid=self.guid)
