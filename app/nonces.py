'''
@since: 13 Aug 2016
@author: oblivion
'''
from datetime import datetime, timedelta
from flask import current_app
import uuid


class Nonces(object):
    '''
    A nonce
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.nonces = dict()

    def add(self, value=None, timeout=(datetime.now() + timedelta(hours=2)),
            ntype=0, nonce=uuid.uuid4().hex):
        '''
        Add a nonce.
        '''
        self.expire()
        if not self.is_active(nonce):
            self.nonces[nonce] = dict()
            self.nonces[nonce]['timeout'] = timeout
            self.nonces[nonce]['value'] = value
            self.nonces[nonce]['type'] = ntype

        return(nonce)

    def new(self, value=None, timeout=(datetime.now() + timedelta(hours=2)),
            ntype=0):
        '''
        Add a new nonce.
        '''
        nonce = uuid.uuid4().hex
        while self.is_active(nonce):
            nonce = uuid.uuid4().hex

        self.add(value=value, timeout=timeout, ntype=ntype, nonce=nonce)

        return(nonce)

    def is_active(self, nonce):
        '''
        Return true if nonce is active-
        '''
        self.expire()
        return(nonce in self.nonces.keys())

    def get(self, nonce):
        '''
        Get the value of a nonce of None.
        '''
        if (self.is_active(nonce)):
            return(self.nonces[nonce])

        return(None)

    def free(self, nonce):
        '''
        Free a nonce.
        '''
        if (self.is_active(nonce)):
            del self.nonces[nonce]
            return(True)

        return(False)

    def expire(self):
        '''
        Expire old nonces.
        '''
        # Don't ever call a function like self.is_active that calls this, or
        # you will loop endlessly.

        # List of expired nonces.
        expired = list()
        for nonce, options in self.nonces.items():
            if options['timeout'] is not None:
                if datetime.now() > options['timeout']:
                    expired.append(nonce)

        nonce = None
        for nonce in expired:
            current_app.logger.debug('Expireing nonce: ' + nonce)
            del self.nonces[nonce]

    def get_dict(self):
        ret = dict()
        for nonce, data in self.nonces.items():
            ret[nonce] = dict()
            if data['timeout'] is not None:
                ret[nonce]['timeout'] = data['timeout'].timestamp()
            else:
                ret[nonce]['timeout'] = None
            if data['value'] is not None:
                ret[nonce]['value'] = data['value'].get_dict()
            else:
                ret[nonce]['value'] = None
            ret[nonce]['type'] = data['type']

        return(ret)

    def len(self):
        return(len(self.nonces))
