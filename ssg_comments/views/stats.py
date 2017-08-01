'''
@since: 15 Aug 2016
@author: oblivion
'''
from flask import current_app
from flask import render_template
from flask.views import MethodView

import ssg_comments


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
        return render_template('stats.html', form=ssg_comments.FORM_NONCES.len(),
                               commit=ssg_comments.COMMIT_NONCES.len(),
                               msg=ssg_comments.MSG_NONCES.len())
