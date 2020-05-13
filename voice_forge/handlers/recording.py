from flask_smorest import Blueprint, abort
from .commons import RegisteredUserMethodView
from ..schemas import AudioData

recordings_blp = Blueprint("recordings", __name__, url_prefix="/recordings",
                           description="Handlers for corpora recording")


@recordings_blp.route("/utterance/<utt_id>")
class UtteranceRecordingHandler(RegisteredUserMethodView):

    @recordings_blp.response(AudioData)
    def get(self, utt_id: str):
        pass

    @recordings_blp.arguments(AudioData, as_kwargs=True)
    def post(self, utt_id: str, audio: bytes, format: str):
        pass

    def delete(self, utt_id: str):
        pass
