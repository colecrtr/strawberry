import atrium
from django.conf import settings


class MXAtriumAPI(atrium.AtriumClient):
    package = atrium


mx_atrium_api = MXAtriumAPI(
    api_key=settings.MX_ATRIUM_API_KEY,
    client_id=settings.MX_ATRIUM_CLIENT_ID,
    environment=settings.MX_ATRIUM_API_URL,
)
