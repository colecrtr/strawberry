import logging
from typing import Callable
from typing import Iterator
from typing import Type
from typing import TypeVar

import atrium
from django.conf import settings


logger = logging.getLogger(__name__)

_MXAtriumTypeVar = TypeVar("_MXAtriumTypeVar", atrium.User, atrium.Member)


class MXAtriumAPI(atrium.AtriumClient):
    MAX_RECORDS_PER_PAGE = 100

    @staticmethod
    def get_objects_generator(
        list_method: Callable, data_key: str, obj_type: Type[_MXAtriumTypeVar]
    ) -> Iterator[_MXAtriumTypeVar]:
        """Gets generator that paginates through the given list_method

        :param list_method: MX Atrium method to paginate
        :param data_key: Location of the list of obj_types is in API response
        :param obj_type: Type of objects being yielded
        :return: Generator of the given obj_type
        """
        page = 1

        while True:
            response = list_method(
                page=page, records_per_page=MXAtriumAPI.MAX_RECORDS_PER_PAGE
            )
            objects: list[_MXAtriumTypeVar] = getattr(response, data_key)

            for obj in objects:
                yield obj

            page += 1
            if page > response.pagination.total_pages:
                logger.info(
                    f"Iterated through {response.pagination.total_entries} MX Atrium "
                    f"{obj_type.__name__}s"
                )
                break

    def get_connect_widget_url(self, user_guid: str) -> None:
        """Gets the URL used by the MX Atrium Connect Widget, unique to the User

        :param user_guid: User.guid
        :return: None
        """
        response: atrium.ConnectWidgetResponseBody = (
            self.connect_widget.get_connect_widget(
                user_guid=user_guid,
                body=atrium.ConnectWidgetRequestBody(),
            )
        )
        connect_widget = response.user
        connect_widget_url = connect_widget.connect_widget_url
        assert user_guid == connect_widget.guid

        logger.info(f"MX Atrium Connect Widget URL generated (for {user_guid})")

        return connect_widget_url

    def get_institution(self, code: str) -> atrium.Institution:
        """Gets an institution by its code

        :param code: A unique identifier for each institution, defined by MX
        :return: MX Atrium Institution
        """

        response: atrium.InstitutionResponseBody = self.institutions.read_institution(
            institution_code=code
        )
        institution = response.institution

        logger.info(f"MX Atrium Institution retrieved ({institution.code})")

        return institution

    def create_user(self, identifier: str, is_disabled: bool) -> atrium.User:
        """Creates an MX Atrium User

        :param identifier: A unique, enforced identifier for the user, defined by you
        :param is_disabled: True if you want the user disabled, false otherwise
        :return: MX Atrium User
        """
        response: atrium.UserCreateRequestBody = self.users.create_user(
            body=atrium.UserCreateRequestBody(
                user={
                    "identifier": identifier,
                    "is_disabled": is_disabled,
                }
            )
        )
        user = response.user

        logger.info(f"MX Atrium User created ({user.guid})")

        return user

    def get_users(self) -> Iterator[atrium.User]:
        """Gets a generator of MX Atrium Users managed by the auth'd client

        :return: Generator of MX Atrium Users
        """
        return self.__class__.get_objects_generator(
            list_method=self.users.list_users, data_key="users", obj_type=atrium.User
        )

    def get_members(self) -> Iterator[atrium.Member]:
        """Gets a generator of MX Atrium Members managed by the auth'd client

        :return: Generator of MX Atrium Members
        """
        return self.__class__.get_objects_generator(
            list_method=self.members.list_members,
            data_key="members",
            obj_type=atrium.Member,
        )


mx_atrium_api = MXAtriumAPI(
    api_key=settings.MX_ATRIUM_API_KEY,
    client_id=settings.MX_ATRIUM_CLIENT_ID,
    environment=settings.MX_ATRIUM_API_URL,
)
