from datetime import datetime
from typing import List

from mongoengine import Document, StringField, ListField, FileField, DateTimeField, ReferenceField


class Corpus(Document):
    meta = {'allow_inheritance': True,
            'abstract': True}

    name = StringField(required=True)
    words = ListField(StringField())

    def make_utterances(self) -> List['UtteranceAssigment']:
        raise NotImplemented()


class TheWordIsCorpus(Corpus):

    language = StringField(default="fr")

    presentation_sentence = {
        "fr": "Le mot est : ",
        "en": "The word is : "
    }

    def make_utterances(self) -> List['UtteranceAssigment']:
        return [
            self.presentation_sentence[self.language] + word
            for word in self.words
        ]


class Recording(Document):
    audio_file = FileField(required=True)
    mime_type: str = StringField(required=True)
    creation_time = DateTimeField(default=datetime)


class UtteranceAssigment(Document):
    # audio file is added once the recording is done
    recordings = ListField(ReferenceField(Recording))
    utterance = StringField(required=True)

    @property
    def has_recordings(self):
        return bool(self.recordings)


class CorpusAssigment(Document):
    recorder = ReferenceField('User', required=True)
    corpus = ReferenceField(Corpus, required=True)
    recorded_files = ListField(ReferenceField(UtteranceAssigment))
