'''
Created on 13 Aug 2016

@author: oblivion
'''
import json
from datetime import datetime


class PostedComment(object):
    '''
    Class that holds comment data until commit
    '''
    def __init__(self, mid=0, ip=None, post='', subject='',
                 tid='', name='', email='', date='', message=''):
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

    def get_dict(self):
        ret = dict()
        ret['mid'] = self.mid
        ret['ip'] = self.ip
        ret['post'] = self.post
        ret['subject'] = self.subject
        ret['tid'] = self.tid
        ret['name'] = self.name
        ret['email'] = self.email
        if self.date == 0:
            ret['date'] = 0
        else:
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
