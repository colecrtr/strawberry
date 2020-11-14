from django.urls import path

from . import views


app_name = "mx_atrium"
urlpatterns = [
    path(
        "connect_widget", view=views.ConnectWidgetView.as_view(), name="connect-widget"
    )
]
