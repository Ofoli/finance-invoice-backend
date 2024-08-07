from http import HTTPStatus
from flask import request, abort
from flask.views import MethodView

from ..models.user import AuthUser


class IsAuthedUserMixin(MethodView):
    user: int

    def dispatch_request(self, *args, **kwargs):
        auth = request.headers.get("Authorization")
        if auth is None:
            abort(HTTPStatus.UNAUTHORIZED, "Unauthorized")
        auth_token = auth.split("Bearer ")[1]
        response: int | str = AuthUser.decode_auth_token(auth_token)
        if isinstance(response, str):
            abort(HTTPStatus.FORBIDDEN, response)

        self.user = response
        return super().dispatch_request(*args, **kwargs)
