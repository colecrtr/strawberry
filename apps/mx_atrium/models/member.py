import datetime
import logging
from typing import TypedDict

from django.db import models
from django.utils.dateparse import parse_datetime
from django.utils.translation import gettext_lazy as _

from apps.mx_atrium.api import mx_atrium_api
from project.models import BaseModel

from .institution import Institution
from .user import User


logger = logging.getLogger(__name__)


class MemberManager(models.Manager):
    class UpdateOrCreateDefaults(TypedDict):
        institution: Institution
        user: User
        aggregated_at: datetime.datetime
        connection_status: str
        name: str
        successfully_aggregated_at: datetime.datetime

    def update_or_create_from_mx_atrium(self, user: User):
        """Updates or creates MX Atrium Members of a User in our database to match theirs"""

        for member_data in mx_atrium_api.get_members(user_guid=user.guid):
            user = User.objects.get(guid=member_data.user_guid)

            institution, created = Institution.objects.get_or_create_from_mx_atrium(
                code=member_data.institution_code
            )

            member, created = self.update_or_create(
                guid=member_data.guid,
                defaults=MemberManager.UpdateOrCreateDefaults(
                    institution=institution,
                    user=user,
                    aggregated_at=parse_datetime(member_data.aggregated_at),
                    connection_status=Member.ConnectionStatus[
                        member_data.connection_status
                    ],
                    name=member_data.name,
                    successfully_aggregated_at=parse_datetime(
                        member_data.successfully_aggregated_at
                    ),
                ),
            )
            logger.info(f"{'Created' if created else 'Updated'} {member}")


class Member(BaseModel):
    """MX Atrium Member

    Docs: https://atrium.mx.com/docs#members
    """

    objects = MemberManager()

    class ConnectionStatus(models.TextChoices):
        CHALLENGED = "CHA", _("Challenged")
        CONNECTED = "CON", _("Connected")

    institution = models.ForeignKey(
        to="mx_atrium.Institution",
        on_delete=models.PROTECT,
        verbose_name=_("MX Atrium Institution"),
    )
    user = models.ForeignKey(
        to="mx_atrium.User",
        on_delete=models.CASCADE,
        verbose_name=_("MX Atrium User"),
    )

    # MX Atrium fields (docs: https://atrium.mx.com/docs#member-fields)
    # - `identifier` is `id`/`pk`
    # - `institution_code` is substituted by `institution` above
    # - `user_guid` is substituted by `user` above
    # - `is_being_aggregated` is unused because it is time-sensitive to active requests
    # - `oauth_window_uri` is unused because it is time-sensitive to active requests
    aggregated_at = models.DateTimeField(
        verbose_name=_("MX Atrium aggregated_at"),
        help_text=_("The date and time the account was last aggregated."),
    )
    connection_status = models.CharField(
        max_length=3,
        choices=ConnectionStatus.choices,
        verbose_name=_("MX Atrium connection_status"),
        help_text=_("The status of a member's aggregation."),
    )
    guid = models.CharField(
        max_length=256,
        unique=True,
        verbose_name=_("MX Atrium guid"),
        help_text=_("A unique identifier for the member. Defined by MX."),
    )
    name = models.CharField(
        max_length=256,
        verbose_name=_("MX Atrium name"),
        help_text=_(
            "The name of the member. If omitted as a parameter when creating the member, the "
            'institution name within the MX platform will be used, e.g., "Chase Bank."'
        ),
    )
    successfully_aggregated_at = models.DateTimeField(
        verbose_name=_("MX Atrium successfully_aggregated_at"),
        help_text=_("The date and time the member was successfully aggregated."),
    )

    def __str__(self) -> str:
        return self.guid
