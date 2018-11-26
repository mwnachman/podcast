import json

import flask
from flask import Blueprint, request, session

from podcast.podcast_app import db
from podcast.models.clients import Superuser
import podcast.svcs.app
from podcast.utils import crossdomain

bp = Blueprint('main', __name__)


@bp.route('/podcasts/top/<number>', methods=['GET'])
@crossdomain()
def top_podcasts(number):
	podcasts = podcast.svcs.app.get_top_podcasts(number)
	return flask.Response(json.dumps(podcasts), mimetype='application/json')
