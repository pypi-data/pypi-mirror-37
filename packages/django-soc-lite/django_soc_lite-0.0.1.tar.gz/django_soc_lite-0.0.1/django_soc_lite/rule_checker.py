import os.path
import json
import re

def sql_replace(query):
    """custom method for match and replace some vulnerable sql characters"""
    for item in get_rule():
        tag = item['tags']['tag'][0]
        if  tag == 'sqli':
            rules = item['rule']
            regex = re.compile(rules)
            if regex.search(query):
                query = regex.sub('', query)
    return query

def get_rule():
    """load rules pattern from rules.json"""
    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, 'rules.json'), 'r') as rule_data:
        data = json.load(rule_data)
    return data

def converter(query):
    """method for decoding urls <query>:<str>"""
    try:
        from . import url_coder
    except ImportError:
        import url_coder
    query = url_coder.decoder(str(query))
    return query

def xss_filter(query):
    """checking input with xss rules"""
    query = converter(query)
    flag = 0
    for item in get_rule():
        tag = item['tags']['tag'][0]
        if  tag == 'xss' or tag == 'dos':
            rules = item['rule']
            regex = re.compile(rules)
            if regex.search(query):
                flag = 1
                description = item['description']
    if flag == 0:
        return False
    return True, description

def sql_filter(query):
    """checking input with sqli rules"""
    query = converter(query)
    flag = 0
    for item in get_rule():
        tag = item['tags']['tag'][0]
        if  tag == 'sqli':
            rule = item['rule']
            regex = re.compile(rule)
            if regex.search(query):
                flag = 1
                description = item['description']
    if flag == 0:
        return False
    return True, description

def dt_filter(query):
    """checking input with directory traversal rules"""
    query = converter(query)
    flag = 0
    for item in get_rule():
        tag = item['tags']['tag'][0]
        if  tag == 'dt' or tag == 'files':
            rule = item['rule']
            regex = re.compile(rule)
            if regex.search(query):
                flag = 1
                description = item['description']
    if flag == 0:
        return False
    return True, description
