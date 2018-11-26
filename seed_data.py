""" Create test database """
__author__ = 'Meredith Latasa <meredith@orionlabs.io>'
__copyright__ = 'Copyright 2018 Orion Labs, Inc.'
__license__ = 'All rights reserved. Do not redistribute.'

import json
import os
import sys

import click

from podcast.podcast_app import create_app, db

def get_static_db():
    static_db_path = ''
    static_db_dir = 'static_db'
    bots_json = 'bots.json'
    speech_services_json = 'speech_services.json'
    clients_json = 'clients.json'

    if os.path.exists(static_db_dir):
        static_db_path = static_db_dir
    if not static_db_path:
        raise Exception('Could not find static_db dir.')

    bots_json_path = os.path.join(static_db_dir, bots_json)
    speech_services_json_path = os.path.join(static_db_dir, speech_services_json)
    clients_json_path = os.path.join(static_db_dir, clients_json)

    with open(bots_json_path, 'r') as bots_json_fd:
        bots_file_json = json.load(bots_json_fd)
        bots = bots_file_json['bots']
        bot_types = bots_file_json['bot_types']
    with open(speech_services_json_path, 'r') as speech_services_json_fd:
        speech_services_json = json.load(speech_services_json_fd)
        speech_services = speech_services_json['speech_services']
        speech_service_keys = speech_services_json['speech_service_keys']
    with open(clients_json_path, 'r') as clients_json_fd:
        clients_file_json = json.load(clients_json_fd)
        superusers = clients_file_json['superusers']

    return bots, bot_types, speech_service_keys, speech_services, superusers

# adds bots to the bots table
def add_bots(bots):
    from podcast.models.bots import Bot
    for bot in bots:
        bot_to_add = Bot(id=bot['id'], name=bot['name'])
        db.session.add(bot_to_add)
    db.session.commit()

def add_speech_service_keys(speech_service_keys):
    from podcast.models.speech import SpeechServiceKey
    for key in speech_service_keys:
        key_to_add = SpeechServiceKey(id=key['id'], key=key['key'])
        db.session.add(key_to_add)
    db.session.commit()

# adds speech services to the speech_services table
def add_speech_services(speech_services):
    from podcast.models.speech import SpeechService, SpeechServiceKey
    speech_service_keys_in_db = db.session.query(SpeechServiceKey).all()
    for service in speech_services:
        service_keys = service['keys']
        member_keys = []
        for key in speech_service_keys_in_db:
            for service_key in service_keys:
                if key.id == service_key['speech_service_key_id']:
                    member_keys.append(key)
        service_to_add = SpeechService(id=service['id'], name=service['name'], speech_service_keys=member_keys)
        db.session.add(service_to_add)
    db.session.commit()

# adds bot_types to the bot_types table
def add_bot_types(bot_types, speech_services):
    from podcast.models.bots import Bot, BotType
    from podcast.models.speech import SpeechServiceKey
    bots_in_db = db.session.query(Bot).all()
    speech_service_keys_in_db = db.session.query(SpeechServiceKey).all()
    for bot_type in bot_types:
        member_bots = []
        member_keys = []
        for bot in bots_in_db:
            if bot.id in bot_type['bots']:
                member_bots.append(bot)
        for speech_service in speech_services:
            service_keys = speech_service['keys']
            for service_key in service_keys:
                for key in speech_service_keys_in_db:
                    if key.id == service_key['speech_service_key_id'] and bot_type['id'] == service_key['bot_type_id']:
                        member_keys.append(key)
        bot_type_to_add = BotType(
                            id=bot_type['id'],
                            name=bot_type['name'],
                            bots=member_bots,
                            speech_service_keys=member_keys)
        db.session.add(bot_type_to_add)
    db.session.commit()

# adds superusers to the superusers table
def add_superusers(superusers):
    from podcast.models.clients import Superuser
    for user in superusers:
        super_user = Superuser(id=user['id'])
        db.session.add(super_user)
    db.session.commit()

def main():
    entities = get_static_db()
    bots, bot_types, speech_service_keys, speech_services, superusers = entities
    add_bots(bots)
    add_speech_service_keys(speech_service_keys)
    add_speech_services(speech_services)
    add_bot_types(bot_types, speech_services)
    add_superusers(superusers)

def init_db(config_name):
    from podcast.models.bots import Bot, BotType
    from podcast.models.speech import SpeechServiceKey
    from podcast.models.clients import Superuser

    app = create_app(config_name)
    app_context = app.app_context()
    app_context.push()

    db.session.remove()
    db.drop_all()
    db.create_all()
    click.echo('Initialized the database.')

if __name__ == '__main__':
    init_db('development')
    main()
