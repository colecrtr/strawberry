import logging

from django.shortcuts import render
from django.views import View

from .models import User


logger = logging.getLogger(__name__)


class ConnectWidgetView(View):
    def get(self, request):
        user, _created = User.objects.get_or_create_from_mx_atrium(
            account_user=request.user
        )
        connect_widget_url = user.get_connect_widget_url()

        logger.info(
            f"Serving MX Atrium Connect Widget for {request.user.username} ({request.user.pk})"
        )

        return render(
            request, "mx_atrium/widget.j2", {"connect_widget_url": connect_widget_url}
        )
