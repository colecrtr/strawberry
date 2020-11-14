import logging

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.account.models import User as AccountUser
from project.models import BaseModel

from .api import mx_atrium_api


logger = logging.getLogger(__name__)


class UserManager(models.Manager):
    def get_or_create_from_account_user(self, account_user: AccountUser) -> "User":
        try:
            return self.get(account_user=account_user)
        except self.model.DoesNotExist:
            response = mx_atrium_api.users.create_user(
                body=mx_atrium_api.package.UserCreateRequestBody(
                    user={
                        "identifier": str(account_user.pk),
                        "is_disabled": not account_user.is_active,
                    }
                )
            )
            user: mx_atrium_api.package.User = response.user

            logger.info(
                f"MX Atrium User ({user.guid}) created for {account_user.username} "
                f"({account_user.pk})"
            )

            return self.create(
                account_user=account_user,
                guid=user.guid,
                is_disabled=user.is_disabled,
            )


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
        help_text=_("A unique identifier, defined by MX"),
    )
    is_disabled = models.BooleanField(
        verbose_name=_("MX Atrium is_disabled"),
        help_text=_("True if you want the user disabled, false otherwise"),
    )

    def get_connect_widget_url(self) -> str:
        """Gets the URL used in the MX Atrium Connect Widget config

        :return: MX Atrium Connect Widget URL string
        """

        response: mx_atrium_api.package.ConnectWidgetResponseBody = (
            mx_atrium_api.connect_widget.get_connect_widget(
                user_guid=self.guid,
                body=mx_atrium_api.package.ConnectWidgetRequestBody(),
            )
        )
        connect_widget = response.user
        connect_widget_url = connect_widget.connect_widget_url
        assert self.guid == connect_widget.guid

        logger.info(
            f"MX Atrium Connect Widget URL generated for {self.account_user.username} "
            f"({self.account_user.pk})"
        )

        return connect_widget_url
