from flask import request, abort
from flask.views import MethodView

from ..models.user import AuthUser


class IsAuthedUserMixin(MethodView):
    user = None

    def dispatch_request(self, *args, **kwargs):
        auth = request.headers.get("Authorization")
        if auth is None:
            abort(401, "Unauthorized")
        auth_token = auth.split("Bearer ")[1]
        response: int | str = AuthUser.decode_auth_token(auth_token)
        if isinstance(response, str):
            abort(403, response)

        self.user = response
        return super().dispatch_request(*args, **kwargs)
