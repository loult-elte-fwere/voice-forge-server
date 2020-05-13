from cookie_factory import hash_cookie
from flask import request, current_app
from flask.views import MethodView
from flask_smorest import abort
from mongoengine import DoesNotExist
from ..models.users import User


class RandomUserMethodView(MethodView):

    def __init__(self):
        self.user: User = None

    def check_user_type(self):
        """Checking that the user has the right type"""
        pass

    def dispatch_request(self, *args, **kwargs):
        # retrieving the token from the headers
        cookie = request.headers.get("Loult-cookie")
        cookie_hash = hash_cookie(cookie, current_app.config.get("SALT"))
        # retrieve cookie from db
        try:
            self.user = User.objects.get(cookie_hash=cookie_hash)
        except DoesNotExist:
            abort(403, message="Not Authorized")

        try:
            return super().dispatch_request(*args, **kwargs)
        except DoesNotExist:
            abort(404, message="Entity not found in database")


class RegisteredUserMethodView(RandomUserMethodView):

    def __init__(self):
        super().__init__()

    def check_user_type(self):
        assert isinstance(self.user, User)

