from __future__ import absolute_import, division, print_function


saved = {}

_NONE = object()


def patch_item(module, attr, newitem):
    olditem = getattr(module, attr, _NONE)
    if olditem is not _NONE:
        saved.setdefault(module.__name__, {}).setdefault(attr, olditem)
    setattr(module, attr, newitem)


def patch_all():
    os_module = __import__("os")
    from plugin.os import system
    patch_item(os_module, "system", system) 
 
 
    #for cross site scirpting
    xss_module = __import__("xss")
    from plugin.threat.xss import requests
    patch_item(xss_module, "process_request", request)
    
    #for Sql injection
    sql_module=__import__("sql")
    from plugin.threat.sql import requests
    patch_item(sql_module, "process_request", request)
