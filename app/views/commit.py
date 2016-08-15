'''
Created on 13 Aug 2016

@author: oblivion
'''
from app import mcomment

from flask import abort
from flask import current_app
from flask.views import MethodView

import app


class Commit(MethodView):
    '''
    View to commit a comment to the site.
    '''
    # Only support GET requests.
    methods = ['GET']

    def __init__(self):
        '''
        Constructor
        '''
        pass

    def get(self, cnonce):
        '''
        Commit the comment to the ssg site.
        '''
        # Get out early
        if cnonce is None:
            current_app.logger.warning('No cnonce.')
            abort(404)
        if not app.COMMIT_NONCES.is_active(cnonce):
            current_app.logger.warning('Invalid cnonce: ' + cnonce)
            abort(404)

        current_app.logger.info('Commit cnonce: ' + cnonce)

        # Convert to modded comment.
        comment = mcomment.ModdedComment()
        comment.from_dict(app.COMMIT_NONCES.get(cnonce)['value'].get_dict())
        # Add to the right list.
        msg_nonce = app.MSG_NONCES.new(value=comment, timeout=None,
                                       ntype=app.MSG_TYPE)
        current_app.logger.debug('New message nonce: ' + msg_nonce)
        current_app.logger.debug('Data: ' + str(comment.get_dict()))

        app.COMMIT_NONCES.free(cnonce)

        current_app.logger.debug('Moderated messages: ' +
                                 str(app.MSG_NONCES.len()))

        app.MSG_NONCES.get(msg_nonce)['value'].new_mid()
        app.save_json()
        app.MSG_NONCES.get(msg_nonce)['value'].save_markdown()
        return "Comment commited."
