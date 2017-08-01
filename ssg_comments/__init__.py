'''
:since: 13/08/2016
:author: oblivion
'''
import io
import json
import logging
import os.path
from datetime import datetime
from logging import handlers

from flask import Flask, request_started, request, url_for
from flask.views import MethodView

from . import mcomment
from . import nonces
from . import pcomment
from .views import Commit
from .views import Form
from .views import Stats

# Init ssg_comments and config
APP = Flask(__name__)
APP.config.from_envvar('SSG_COMMENTS_CONFIG')
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


def load_json():
    global COMMIT_NONCES

    APP.logger.debug("Loading JSON.")

    if not os.path.isfile(APP.config['QUEUED_MSG_PATH'] + 'state.json'):
        APP.logger.info('No saved date.')
        return

    with io.open(APP.config['QUEUED_MSG_PATH'] + 'state.json', 'r',
                 encoding='utf-8') as json_file:
        json_data = json_file.read()
        if json_data != '':
            json_dict = json.loads(json_data)

            # Load comments awaiting moderation
            cur_post = pcomment.PostedComment()
            for nonce, data in json_dict['commit_nonces'].items():
                APP.logger.debug('Loading commit nonce: ' + nonce)
                if data['timeout'] is None:
                    timeout = None
                else:
                    timeout = datetime.fromtimestamp(data['timeout'])
                COMMIT_NONCES.add(nonce=nonce,
                                  timeout=timeout,
                                  value=None,
                                  ntype=data['type'])
                APP.logger.debug("Data: " + str(data))
                cur_post.from_dict(data['value'])
                COMMIT_NONCES.nonces[nonce]['value'] = cur_post

            # Load active form nonces
            for nonce, data in json_dict['form_nonces'].items():
                APP.logger.debug('Loading form nonce: ' + nonce)
                FORM_NONCES.add(nonce=nonce,
                                timeout=datetime.fromtimestamp(
                                    data['timeout']),
                                value=None,
                                ntype=data['type'])
                APP.logger.debug("Data: " + str(data))

            # Load accepted comment metadata
            cur_comm = mcomment.ModdedComment()
            for nonce, data in json_dict['msg_nonces'].items():
                APP.logger.debug('Loading message nonce: ' + nonce)
                if data['timeout'] is None:
                    timeout = None
                else:
                    timeout = datetime.fromtimestamp(data['timeout'])

                MSG_NONCES.add(nonce=nonce,
                               timeout=timeout,
                               value=None,
                               ntype=data['type'])
                APP.logger.debug("Data: " + str(data))
                cur_comm.from_dict(data['value'])
                MSG_NONCES.nonces[nonce]['value'] = cur_comm

        else:
            APP.logger.warning('Empty JSON data file.')

    json_file.close()


# Start logger
if APP.config['DEBUG']:
    APP.logger.setLevel(logging.DEBUG)
    file_log = handlers.RotatingFileHandler("ssg_comments.log",
                                            maxBytes=10000000,
                                            backupCount=5)
    file_log.setLevel(logging.DEBUG)
    file_log.setFormatter(logging.Formatter('%(asctime)s - %(filename)s - ' +
                                            '%(funcName)s - %(levelname)s: ' +
                                            '%(message)s'))
    APP.logger.addHandler(file_log)
else:
    APP.logger.setLevel(logging.CRITICAL)
    file_log = handlers.RotatingFileHandler("ssg_comments.log",
                                            maxBytes=10000000,
                                            backupCount=5)
    file_log.setLevel(logging.WARNING)
    file_log.setFormatter(logging.Formatter('%(asctime)s - %(filename)s - ' +
                                            '%(funcName)s - %(levelname)s:' +
                                            ' %(message)s'))
    APP.logger.addHandler(file_log)

# Build all URL using configured services from SERVICES.
APP.logger.info('sg_comments')
APP.logger.debug("Building urls.")
FORM = Form.as_view('form')
APP.add_url_rule('/post/<string:post>', view_func=FORM,
                 methods=['GET'])
APP.add_url_rule('/post/', view_func=FORM,
                 methods=['POST'])

APP.add_url_rule('/post/commit/<string:cnonce>',
                 view_func=Commit.as_view('commit'),
                 methods=['GET'])

APP.add_url_rule('/post/stats',
                 view_func=Stats.as_view('stats'),
                 methods=['GET'])

class Test(MethodView):
    '''
    View to show the comment form.
    '''
    # Only support GET and POST requests.
    methods = ['GET']

    def __init__(self):
        '''
        Constructor
        '''
        self.nonce = None

    def get(self):
        '''
        Render the comment form.
        '''
        return('Hello World!')

APP.add_url_rule('/',
                 view_func=Test.as_view('test'),
                 methods=['GET'])


def log_request(sender, **extra):
    sender.logger.debug('Request: ' + str(request))

request_started.connect(log_request, APP)

APP.logger.info('URL map:\n' + str(APP.url_map))

# Load data.
load_json()
