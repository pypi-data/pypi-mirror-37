class CharStream(object):
    
    def open(self):
        pass
    
    def close(self):
        pass
    
    def has_next(self):
        return False
    
    def peek(self):
        return None
    
    def advance(self):
        return None
    
    
class StringStream(CharStream):
    
    def __init__(self, s):
        self._s = s
        self._idx = 0
        
    def has_next(self):
        return self._idx < len(self._s)
    
    def peek(self):
        return self._s[self._idx]
    
    def advance(self):
        ret = self._s[self._idx]
        self._idx += 1
        return ret