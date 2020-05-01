from flask import request
from flask.views import MethodView
from flask_smorest import abort
from mongoengine import DoesNotExist


class RandomUserMethodView(MethodView):

    def __init__(self):
        self.user: User = None

    def check_user_type(self):
        """Checking that the user has the right type"""
        pass

    def dispatch_request(self, *args, **kwargs):
        # retrieving the token from the headers
        token = request.headers.get("Loult-cookie")
        # retrieve cookie from db
        # TODO
        try:
            return super().dispatch_request(*args, **kwargs)
        except DoesNotExist:
            abort(404, message="Entity not found in database")


class AdminMethodView(RandomUserMethodView):

    def __init__(self):
        super().__init__()

    def check_user_type(self):
        pass


class RegisteredUserMethodView(RandomUserMethodView):

    def __init__(self):
        super().__init__()

    def check_user_type(self):
        pass

