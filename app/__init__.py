'''
:since: 01/08/2015
:author: oblivion
'''
from flask import Flask
import io
import json
from logging import handlers
import logging

from app import nonces
from app.views import Commit
from app.views import Form


# Init app and config
APP = Flask(__name__)
APP.config.from_object('config')
CONFIG = APP.config

COMMIT_TYPE = 1
FORM_TYPE = 2
MSG_TYPE = 3

COMMIT_NONCES = nonces.Nonces()
FORM_NONCES = nonces.Nonces()
MSG_NONCES = nonces.Nonces()


def save_json():
    APP.logger.debug("Saving JSON.")
    json_dict = dict()
    json_dict['commit_nonces'] = COMMIT_NONCES.get_dict()
    json_dict['form_nonces'] = FORM_NONCES.get_dict()
    json_dict['msg_nonces'] = MSG_NONCES.get_dict()

    with io.open(APP.config['QUEUED_MSG_PATH'] + 'state.json', 'w',
                 encoding='utf-8') as json_file:
        json_file.write(json.dumps(json_dict,
                                   ensure_ascii=False,
                                   skipkeys=True,
                                   indent=4,
                                   sort_keys=True))
        json_file.close()


# Start logger
if APP.config['DEBUG']:
    APP.logger.setLevel(logging.DEBUG)
    file_log = handlers.RotatingFileHandler("ssg-comments.log",
                                            maxBytes=10000000,
                                            backupCount=5)
    file_log.setLevel(logging.DEBUG)
    file_log.setFormatter(logging.Formatter('%(asctime)s - %(filename)s - ' +
                                            '%(funcName)s - %(levelname)s: ' +
                                            '%(message)s'))
    APP.logger.addHandler(file_log)
else:
    APP.logger.setLevel(logging.CRITICAL)
    file_log = handlers.RotatingFileHandler("ssg-comments.log",
                                            maxBytes=10000000,
                                            backupCount=5)
    file_log.setLevel(logging.WARNING)
    file_log.setFormatter(logging.Formatter('%(asctime)s - %(filename)s - ' +
                                            '%(funcName)s - %(levelname)s:' +
                                            ' %(message)s'))
    APP.logger.addHandler(file_log)

# Build all URL using configured services from SERVICES.
APP.logger.debug("Building urls.")

FORM = Form.as_view('form')
APP.add_url_rule('/post/<string:post>', view_func=FORM,
                 methods=['GET'])
APP.add_url_rule('/post/', view_func=FORM,
                 methods=['POST'])

APP.add_url_rule('/post/commit/<string:cnonce>',
                 view_func=Commit.as_view('commit'),
                 methods=['GET'])
