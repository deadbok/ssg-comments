'''
Created on 13 Aug 2016

@author: oblivion
'''

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

        comment = app.COMMIT_NONCES.get(cnonce)

        return "Comment commited."
