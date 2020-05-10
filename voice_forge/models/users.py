from mongoengine import Document, StringField, ListField, ReferenceField
from cookie_factory import PokeParameters, hash_cookie


class User(Document):
    cookie_hash = StringField(primary_key=True, required=True)
    assigned_corpora = ListField(ReferenceField('CorpusRecording'))

    @property
    def poke_params(self):
        return PokeParameters.from_cookie_hash(self.cookie_hash)


