'''
@since: 13 Aug 2016
@author: oblivion
'''
import uuid
import json

from datetime import datetime, timedelta
from flask import current_app


class Nonces(object):
    '''
    A nonce
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.nonces = dict()

    def add(self, value=None, timeout=datetime.now() + timedelta(hours=2),
            type=0):
        '''
        Add a nonce with a value.
        '''
        self.expire()
        nonce = uuid.uuid4().hex
        while self.is_active(nonce):
            nonce = uuid.uuid4().hex

        self.nonces[nonce] = dict()
        self.nonces[nonce]['timeout'] = timeout
        self.nonces[nonce]['value'] = value
        self.nonces[nonce]['type'] = type

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
        current_app.logger.debug('Removing expired nonces.')
        for nonce, options in self.nonces.items():
            if datetime.now() > options['timeout']:
                current_app.logger.info("Nonce " + nonce + " expired.")
                del self.nonces[nonce]

        current_app.logger.info(str(len(self.nonces)) + " active nonces.")

    def get_dict(self):
        ret = dict()
        for nonce, data in self.nonces.items():
            current_app.logger.debug('Creating json for: ' + nonce + ' - ' +
                                     str(data))

            ret[nonce] = dict()
            ret[nonce]['timeout'] = data['timeout'].isoformat()
            if data['value'] is not None:
                ret[nonce]['value'] = data['value'].get_dict()
            else:
                ret[nonce]['value'] = None
            ret[nonce]['type'] = data['type']

        return(ret)
