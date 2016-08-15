'''
@since: 15 Aug 2016
@author: oblivion
'''
from flask import current_app
from flask import render_template
from flask.views import MethodView

import app


class Stats(MethodView):
    '''
    View to show the comment form.
    '''
    # Only support GET requests.
    methods = ['GET']

    def get(self):
        '''
        Render the status information.
        '''
        app.save_json()

        current_app.logger.debug("Rendering status template.")
        return render_template('stats.html', form=app.FORM_NONCES.len(),
                               commit=app.COMMIT_NONCES.len(),
                               msg=app.MSG_NONCES.len())
