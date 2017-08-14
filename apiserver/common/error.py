class Error(object):
    def __init__(self, code, msg=None, data=None):
        self.code = code
        self.msg = msg
        self.data = data

    def __str__(self):
        err = self.to_dict()
        return str(err)
    
    def to_dict(self):
        err = {}
        err['err_code'] = self.code
        if self.msg:
            err['err_msg'] = self.msg
        if self.data:
            err['data'] = self.data

        return err
    
    def err_code(self):
        return self.code
    
    def err_msg(self):
        return self.msg