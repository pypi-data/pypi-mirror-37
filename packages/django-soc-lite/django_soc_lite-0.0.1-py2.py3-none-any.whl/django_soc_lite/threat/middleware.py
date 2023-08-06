from __future__ import absolute_import, division, print_function

import json
import re
import requests
import traceback
from django.conf import settings
from django.http import QueryDict, HttpResponse, HttpResponseRedirect, HttpRequest
try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote
from ..verify import check

class ThreatEquationMiddleware(object):
    def process_request(self, request):
        if check():
            pass
        else:
            return
        self.request = request
        from ..threat.xss import XSSMiddleware
        XSSMiddleware(self.request)
        from ..threat.sql import SQLMiddleware
        SQLMiddleware(self.request)
        from ..threat.directory_traversal import DTMiddleware
        DTMiddleware(self.request)
        
    def process_response(self, request, response):
        return response
