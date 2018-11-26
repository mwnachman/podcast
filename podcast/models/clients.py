from podcast.podcast_app import db

class Superuser(db.Model):
	__tablename__ = 'superusers'
	id = db.Column(db.String(32), primary_key=True)

	def __init__(self, id):
		self.id = id
