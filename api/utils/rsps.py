class Rsps:
    def __init__(self, code=1, msg='', data=None):
        self.code = code
        self.msg = msg
        self.data = data


    def make(self):
        return {'code':self.code,'msg':self.msg,'data':self.data}