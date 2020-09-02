import base64

from flask_smorest.fields import Upload
from marshmallow import Schema, fields, ValidationError


class Base64Field(fields.Str):
    """Field that serializes to a Base64 string and deserializes to bytes"""

    def _serialize(self, value, attr, obj, **kwargs):
        return base64.encodebytes(value).decode("ascii")

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return base64.b64decode(value)
        except ValueError as error:
            raise ValidationError("Cannot decode b64 encoded string") from error


class AudioUpload(Schema):
    file = Upload(required=True)


class UserProfile(Schema):
    pokename = fields.Str(required=True)
    adj = fields.Str(required=True)
    color = fields.Str(required=True)
    img = Base64Field()


class CorpusSummary(Schema):
    name = fields.String()
    id = fields.String()
    total_utt = fields.Int()
    recorded_utt = fields.Int()


class UtteranceAssignment(Schema):
    id = fields.String(required=True)
    recordings = fields.List(fields.Nested(AudioUpload))


class CorpusFull(CorpusSummary):
    utterances = fields.List(fields.Nested(UtteranceAssignment))
