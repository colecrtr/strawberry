from django.contrib.auth.models import AbstractUser

from project.models import BaseModel


class User(AbstractUser, BaseModel):
    """Users of this application (auth.User)"""

    pass
