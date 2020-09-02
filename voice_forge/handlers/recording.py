import logging
from io import BytesIO

import magic
from flask_smorest import Blueprint, abort
from pydub import AudioSegment
from werkzeug.datastructures import FileStorage

from .commons import RegisteredUserMethodView
from ..schemas import AudioUpload

recordings_blp = Blueprint("recordings", __name__, url_prefix="/recordings",
                           description="Handlers for corpora recording")


@recordings_blp.route("/utterance/<utt_id>")
class UtteranceRecordingHandler(RegisteredUserMethodView):

    def get(self, utt_id: str):
        pass

    @recordings_blp.arguments(AudioUpload, location='files', as_kwargs=True)
    def post(self, utt_id: str, file: FileStorage):

        # first checking the audio file
        payload: bytes = file.read()
        mime_type = magic.from_buffer(payload, mime=True)
        mime_main_type = mime_type.split("/")[0]
        buffer = BytesIO(payload)
        if mime_main_type == "audio":
            try:
                try:
                    AudioSegment.from_file(buffer)
                except MemoryError:
                    AudioSegment.from_file_using_temporary_files(buffer)
            except Exception as e:
                logging.warning(f"Error while decoding audio file : {str(e)}")
                return abort("Invalid audio file")
        else:
            logging.warning(f"Invalid submission with mime type : {mime_type}")
            raise abort("Invalid mime type for audio file")

        # then saving it

    def delete(self, utt_id: str):
        pass
