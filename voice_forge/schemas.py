from marshmallow import Schema, fields, ValidationError


class BytesField(fields.Field):
    def _validate(self, value):
        if not isinstance(value, bytes):
            raise ValidationError('Invalid input type.')

        if value is None or value == b'':
            raise ValidationError('Invalid value')


class AudioData(Schema):
    audio = BytesField(required=True)
    format = fields.Str(required=True)
    record_time = fields.DateTime()


class UserProfile(Schema):
    pokename = fields.Str(required=True)
    adj = fields.Str(required=True)
    color = fields.Str(required=True)
    img = BytesField()


class CorpusSummary(Schema):
    name = fields.String()
    id = fields.String()
    total_utt = fields.Int()
    recorded_utt = fields.Int()


class UtteranceAssignment(Schema):
    id = fields.String(required=True)
    recordings = fields.List(fields.Nested(AudioData))


class CorpusFull(CorpusSummary):
    utterances = fields.List(fields.Nested(UtteranceAssignment))