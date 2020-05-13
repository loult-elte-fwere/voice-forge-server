from flask_smorest import Blueprint, abort
from .commons import RegisteredUserMethodView
from ..schemas import UserProfile, CorpusSummary, CorpusFull

account_blp = Blueprint("account", __name__, url_prefix="/account",
                        description="Handlers for user account data")


@account_blp.route("/profile")
class GetUserProfileHandler(RegisteredUserMethodView):

    @account_blp.response(UserProfile)
    def get(self):
        pass


@account_blp.route("/corpora")
class GetActiveCorporaHandler(RegisteredUserMethodView):

    @account_blp.response(CorpusSummary(many=True))
    def get(self):
        pass


@account_blp.route("/corpus/list")
class ListCorpusRecordingsHandler(RegisteredUserMethodView):

    @account_blp.response(CorpusFull)
    def get(self):
        pass


