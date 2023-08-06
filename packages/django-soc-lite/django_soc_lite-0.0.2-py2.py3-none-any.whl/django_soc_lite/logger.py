"""Bug fix log generator and api calling"""
import json
import logging
import requests
from . import django_server
#token headers will be added....

class StructuredMessage(object):
    """method for catch and generate log event"""
    def __init__(self, name, **kwargs):
        self.name = name
        self.kwargs = kwargs
        if self.name == 'attack':
            r = requests.post(django_server, json=self.kwargs)
        else:
            pass
        
    def __str__(self):
        return json.dumps(self.kwargs)

# optional, to improve readability
log = StructuredMessage
logging.basicConfig(level=logging.INFO, format='%(message)s')
