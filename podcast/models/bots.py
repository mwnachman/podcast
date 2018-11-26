from podcast.podcast_app import db

class Bot(db.Model):
    __tablename__ = 'bots'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False, index=True)
    bot_type = db.Column(db.ForeignKey('bot_types.id'))

    def __init__(self, id, name):
        self.id = id
        self.name = name

class BotType(db.Model):
    __tablename__ = 'bot_types'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    bots = db.relationship('Bot', backref='bottype')
    speech_service_keys = db.relationship('SpeechServiceKey', backref='bottype')

    def __init__(self, id, name, bots, speech_service_keys):
        self.id = id
        self.name = name
        self.bots = bots
        self.speech_service_keys = speech_service_keys
