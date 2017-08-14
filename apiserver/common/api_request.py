from constants import API_REQUEST_TYPE

class APIRequest(object):
    def __init__(self, rtype, headers, params, **kwargs):
        self.rtype = rtype
        self.headers = headers
        self.params = params
        self.action = self._get_action()
        self.identity = self._get_identity()
        self.remote_addr = self._get_remote_addr()
        self.method = self.headers.get('method', '')

    def __str__(self):
        return (('type:(%s) action:(%s) identity:(%s) remote_addr:(%s) method:(%s)') % (self.rtype, 
                                                                                        self.action, 
                                                                                        self.identity,
                                                                                        self.remote_addr,
                                                                                        self.method))
        
    def _get_action(self):
        return self.params.get('action', '')
    
    def _get_remote_addr(self):
        return self.headers.get('remote_addr', '')
    
    def _get_identity(self):
        if self.rtype == API_REQUEST_TYPE:
            return self.params.get('access_key', '')
        
        return ''
        
    def build_request(self):
        req = {"type": self.rtype,
               "headers": self.headers,
               "params": self.params}
        return req
