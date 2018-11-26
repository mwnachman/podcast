from podcast.podcast_app import db

class SpeechServiceKey(db.Model):
    __tablename__ = 'speech_service_keys'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(64), unique=True)
    bot_type_id = db.Column(db.ForeignKey('bot_types.id'))
    speech_service_id = db.Column(db.ForeignKey('speech_services.id'))

    def __init__(self, id, key):
        self.id = id
        self.key = key

class SpeechService(db.Model):
    __tablename__ = 'speech_services'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    speech_service_keys = db.relationship('SpeechServiceKey', backref='speech_service')

    def __init__(self, id, name, speech_service_keys):
        self.id = id
        self.name = name
        self.speech_service_keys = speech_service_keys
