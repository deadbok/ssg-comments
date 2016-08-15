'''
Created on 13 Aug 2016

@author: oblivion
'''
from datetime import datetime
from flask import current_app
import io
import uuid


class ModdedComment(object):
    '''
    Class that holds comment data until commit
    '''
    def __init__(self, mid=uuid.uuid1().hex, ip=None, post='', subject='',
                 tid=0, name='', email='', date='', message=''):
        '''
        Constructor
        '''
        self.mid = mid
        self.ip = ip
        self.post = post
        self.subject = subject
        self.tid = tid
        self.name = name
        self.email = email
        self.date = date
        self.message = message
        self.filename = str(self.mid) + '_' + str(self.tid) + '.md'

    def new_mid(self):
        self.mid = uuid.uuid1().hex
        self.filename = str(self.mid) + '_' + str(self.tid) + '.md'

    def get_dict(self):
        ret = dict()
        ret['mid'] = self.mid
        ret['ip'] = self.ip
        ret['post'] = self.post
        ret['subject'] = self.subject
        ret['tid'] = self.tid
        ret['name'] = self.name
        ret['email'] = self.email
        ret['date'] = self.date.timestamp()
        ret['message'] = self.message

        return(ret)

    def from_dict(self, comment):
        '''
        Populate from a dictionary.
        '''
        self.__init__(mid=comment['mid'],
                      ip=comment['ip'],
                      post=comment['post'],
                      subject=comment['subject'],
                      tid=comment['tid'],
                      name=comment['name'],
                      email=comment['email'],
                      date=datetime.fromtimestamp(comment['date']),
                      message=comment['message'])

    def save_markdown(self):
        '''
        Save comment to Markdown file.
        '''
        current_app.logger.debug("Saving MarkDown for mid: " + self.mid)
        content = ('mid: ' + str(self.mid) + '\ntid: ' + str(self.tid) +
                   '\npost: ' + self.post + '\nsubject: ' + self.subject +
                   '\nname: ' + self.name + ' \ne-mail: ' + self.email +
                   '\nip: ' + self.ip + '\ndate: ' + self.date.isoformat() +
                   '\ntype: comment' + '\n\n' + self.message)

        with io.open(current_app.config['MODDED_MSG_PATH'] + self.filename,
                     'w', encoding='utf-8') as markdown_file:
            markdown_file.write(content)
            markdown_file.close()
