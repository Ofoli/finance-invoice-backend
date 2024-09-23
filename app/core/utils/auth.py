from http import HTTPStatus
from flask import request, abort
from flask.views import MethodView

from app.core.models.user import AuthUser
from app.core.constants import WHITELISTED_IPS


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


class IsIPWhitelistedMixin(MethodView):
    def dispatch_request(self, *args, **kwargs):
        source_ip = request.remote_addr
        if request.headers.getlist("X-Forwarded-For"):
            source_ip = request.headers.getlist("X-Forwarded-For")[0]

        if source_ip not in WHITELISTED_IPS.split(","):
            abort(HTTPStatus.FORBIDDEN)

        return super().dispatch_request(*args, **kwargs)
