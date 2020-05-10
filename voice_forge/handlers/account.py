from flask_smorest import Blueprint, abort
from .commons import RegisteredUserMethodView

account_blp = Blueprint("account", __name__, url_prefix="/account",
                           description="Handlers for user account data")


@account_blp.route("/profile")
class GetUserProfileHandler(RegisteredUserMethodView):
    pass


@account_blp.route("/corpora")
class GetActiveCorporaHandler(RegisteredUserMethodView):
    pass


@account_blp.route("/corpus/list")
class ListCorpusRecordingsHandler(RegisteredUserMethodView):
    pass


