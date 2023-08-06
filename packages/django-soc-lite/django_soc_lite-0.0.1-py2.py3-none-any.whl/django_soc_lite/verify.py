"""Client's access verification"""
import json
import requests
import requests_cache
from . import client_id, secret, verify_url

requests_cache.install_cache('response_cache', expire_after=86400)

def verify():
    """return True if valid access else False"""
    data = {'product_id': client_id, 'api_token': secret}
    response = requests.post(verify_url, json=data)
    if str(response.text) == '"trial"' or str(response.text) == '"paid"':
        return True
    else:
        return False
def check():
    """False if client_id not set, else True"""
    if client_id == 'n/a' or secret == 'n/a':
        return False
    return verify()
