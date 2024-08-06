import logging
from http import HTTPStatus

from app.core.constants import APP_LOGGER
from ..users.queries import get_user_by_email
from ..utils.response import Response
from ..schemas.user import AuthUserSchema

logger = logging.getLogger(APP_LOGGER)


class Auth:

    @staticmethod
    def login_user(email: str, password: str):
        try:
            user = get_user_by_email(email=email)
            if user is not None and user.check_password(password):
                auth_token = user.generate_auth_token()
                response = dict(user=AuthUserSchema().dump(
                    user), token=auth_token)
                return Response().success(response)
            else:
                response = 'email or password does not match.'
                return Response(HTTPStatus.PRECONDITION_FAILED).failed(response)

        except Exception as e:
            logger.error("Login failed for {}, Error: {}".format(email, e))
            return Response(HTTPStatus.INTERNAL_SERVER_ERROR).failed("Try Again")
