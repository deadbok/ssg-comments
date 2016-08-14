'''
Created on 13 Aug 2016

@author: oblivion
'''
import json


class Comment(object):
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
        ret['date'] = self.date.isoformat()
        ret['message'] = self.message

        return(ret)
