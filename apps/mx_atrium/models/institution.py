import logging

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.mx_atrium.api import mx_atrium_api
from project.models import BaseModel


logger = logging.getLogger(__name__)


class InstitutionManager(models.Manager):
    def get_or_create_from_mx_atrium(self, code: str):
        """Gets or creates the MX Atrium Institution with the given `code`"""

        try:
            institution = self.get(code=code)
            created = False
        except self.model.DoesNotExist:
            institution_data = mx_atrium_api.get_institution(code=code)
            institution = self.create(
                code=institution_data.code,
                name=institution_data.name,
                small_logo_url=institution_data.small_logo_url,
                medium_logo_url=institution_data.medium_logo_url,
                url=institution_data.url,
            )
            created = True
            logger.info(f"Created {institution}")

        return institution, created


class Institution(BaseModel):
    """MX Atrium Institution

    Docs: https://atrium.mx.com/docs#institutions
    """

    objects = InstitutionManager()

    # MX Atrium fields (docs: https://atrium.mx.com/docs#institution-fields)
    # - `supports_account_identification` is unused
    # - `supports_account_statement` is unused
    # - `supports_account_verification` is unused
    # - `supports_transaction_history` is unused
    code = models.CharField(
        max_length=256,
        unique=True,
        verbose_name=_("code"),
        help_text=_("A unique identifier for each institution, defined by MX."),
    )
    name = models.CharField(
        max_length=256,
        verbose_name=_("name"),
        help_text=_(
            'An easy-to-read name for an institution, e.g., "Chase Bank" or "Wells Fargo Bank".'
        ),
    )
    small_logo_url = models.URLField(
        verbose_name=_("Small logo URL"),
        help_text=_(
            "URL for a 50px X 50px logo for each institution. A generic logo is returned for "
            "institutions that don't have one."
        ),
    )
    medium_logo_url = models.URLField(
        verbose_name=_("Medium logo URL"),
        help_text=_(
            "URL for a 100px X 100px logo for each institution. A generic logo is returned for "
            "institutions that don't have one."
        ),
    )
    url = models.URLField(
        verbose_name=_("URL"),
        help_text=_("Website URL for a particular institution, e.g., www.chase.com."),
    )

    def __str__(self) -> str:
        return self.code
