from __future__ import absolute_import, division, print_function

import os
location = os.path.expanduser("~")
from django.conf import settings

try:
    client_id = settings.THREAT_EQUATION_PRODUCT_KEY
    secret = settings.THREAT_EQUATION_API_KEY    
except IOError as exc:
    client_id = 'n/a'
    secret = 'n/a'


server = 'https://www.threatequation.com'

plugin_name = 'ThreatequationPythonDjango v0.0.5'
django_server = server + '/api/v1/attack_log/'
verify_url = server + '/api/v1/product_verify/'
port = None
