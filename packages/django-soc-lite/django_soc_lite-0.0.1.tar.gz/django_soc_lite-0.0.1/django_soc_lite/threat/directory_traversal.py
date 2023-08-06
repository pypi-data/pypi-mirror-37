from ..threat.middleware import *
import bleach

from .. import url_coder, rule_checker, HTML_Escape
from ..threat.log_generator import send
def send_log(request, query):
    send(request, "DT", str(query), request.path, 'encoding, Insecure Path detection')

class DTMiddleware(object):
    def __init__(self, request):
        self.request = request
        if self.request.method == 'GET':
            self.get_method()
        if self.request.method == 'POST':
            self.request_data = self.request.POST.copy()
            self.post_method()
        
        if self.request.method == 'PUT':
            self.request_data = self.request.PUT.copy()
            self.post_method()
        
        if self.request.method == 'PATCH':
            self.request_data = self.request.PATCH.copy()
            self.post_method()

    def get_method(self):
        query = self.request.META.get('QUERY_STRING')
        if query:
            q = QueryDict(query)
            dict = q.dict()
            list = [k for k in dict]
            parameter = list[0]
            value = dict[parameter]
            value = url_coder.decoder(str(value))                          #decoding/double/decoding
            if rule_checker.dt_filter(str(value)):                         #check attack 
                send_log(self.request, query)
                return True
            return False
        if not query:
            try:
                path = self.request.path
                import os.path                                    
                org_value = os.path.split(path)[1]                        #last value from path
                value = url_coder.decoder(str(org_value))                  #decoding/double/decoding
                if rule_checker.dt_filter(str(value)):                #check attack
                    send_log(self.request, str(org_value))
                return True
            except:
                return False 
    def post_method(self):
        l = [k for k in self.request_data]
        if not l:
            return
        for i in range(len(l)):
            par = l[i] 
            org_value = self.request_data.get(par)
            value = url_coder.decoder(str(org_value))
            if rule_checker.dt_filter(str(value)): 
                send_log(self.request, str(par+'='+org_value))
